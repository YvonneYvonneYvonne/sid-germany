import matplotlib.pyplot as plt
import pandas as pd
import pytask
import seaborn as sns

from src.config import BLD
from src.config import PLOT_END_DATE
from src.config import PLOT_SIZE
from src.config import PLOT_START_DATE
from src.config import SRC
from src.plotting.plotting import style_plot
from src.prepare_data.task_prepare_virus_variant_data import STRAIN_FILES

_MODULE_DEPENDENCIES = {
    "plotting.py": SRC / "plotting" / "plotting.py",
}


@pytask.mark.depends_on(_MODULE_DEPENDENCIES)
@pytask.mark.depends_on(STRAIN_FILES)
@pytask.mark.produces(
    {
        "b117": BLD / "data" / "virus_strains" / "compare_b117.pdf",
        "delta": BLD / "data" / "virus_strains" / "compare_delta.pdf",
    }
)
def task_plot_comparison_of_virus_variant_data(depends_on, produces):
    data = pd.read_csv(
        depends_on["rki_strains"],
        parse_dates=["date"],
        index_col="date",
    )
    for strain, fig_path in produces.items():
        rki = data[f"share_{strain}"]
        extrapolated = pd.read_pickle(depends_on["virus_shares_dict"])[strain]

        fig, ax = plt.subplots(figsize=PLOT_SIZE)
        for sr, label, style in zip(
            [rki, extrapolated], ["rki", "extrapolated"], ["-", "--"]
        ):
            sr = sr[sr > 0]
            sns.lineplot(x=sr.index, y=sr, label=label, ax=ax, linestyle=style)

        fig, ax = style_plot(fig, ax)
        ax.set_title(f"Share of Virus Variant {strain.title()} Over Time")
        fig.savefig(fig_path)
        plt.close()


@pytask.mark.depends_on(_MODULE_DEPENDENCIES)
@pytask.mark.depends_on(STRAIN_FILES)
@pytask.mark.produces(BLD / "figures" / "data" / "share_of_b117_acc_to_rki.pdf")
def task_plot_virus_variant_data(depends_on, produces):
    rki_b117 = pd.read_csv(
        depends_on["rki_strains"],
        parse_dates=["date"],
        index_col="date",
    )["share_b117"]

    fig, ax = plt.subplots(figsize=PLOT_SIZE)

    sns.lineplot(x=rki_b117.index, y=rki_b117, ax=ax, color="#4e79a7")
    ax.set_xlim(pd.Timestamp(PLOT_START_DATE), pd.Timestamp(PLOT_END_DATE))

    fig, ax = style_plot(fig, ax)
    fig.tight_layout()
    fig.savefig(produces)
    plt.close()
