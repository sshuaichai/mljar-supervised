import os
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
from supervised.utils.metric import Metric
from supervised.utils.config import LOG_LEVEL

logger.setLevel(LOG_LEVEL)

import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class LeaderboardPlots:

    performance_fname = "ldb_performance.png"
    performance_boxplot_fname = "ldb_performance_boxplot.png"

    @staticmethod
    def compute(ldb, model_path, fout):
        if ldb.shape[0] < 2:
            return
        # Scatter plot
        plt.figure(figsize=(10, 7))
        plt.plot(ldb.metric_value, "*", markersize=12, alpha=0.75)
        plt.xlabel("#Iteration")
        plt.ylabel(ldb.metric_type.iloc[0])
        plt.title("AutoML Performance")
        plt.tight_layout(pad=2.0)
        plot_path = os.path.join(model_path, LeaderboardPlots.performance_fname)
        plt.savefig(plot_path)
        plt.close("all")

        fout.write("\n\n### AutoML Performance\n")
        fout.write(f"![AutoML Performance]({LeaderboardPlots.performance_fname})")

        # Boxplot
        by = "model_type"
        column = "metric_value"
        df2 = pd.DataFrame({col: vals[column] for col, vals in ldb.groupby(by)})

        ascending_sort = Metric.optimize_negative(ldb.metric_type.iloc[0])
        mins = df2.min().sort_values(ascending=ascending_sort)

        plt.figure(figsize=(10, 7))
        # plt.title("")
        plt.ylabel(ldb.metric_type.iloc[0])
        df2[mins.index].boxplot(rot=90, fontsize=12)

        plt.tight_layout(pad=2.0)
        plot_path = os.path.join(model_path, LeaderboardPlots.performance_boxplot_fname)
        plt.savefig(plot_path)
        plt.close("all")

        fout.write("\n\n### AutoML Performance Boxplot\n")
        fout.write(
            f"![AutoML Performance Boxplot]({LeaderboardPlots.performance_boxplot_fname})"
        )

        fairness_metrics = [f for f in ldb.columns if "fairness_" in f and f != "fairness_metric"]
        for fm in fairness_metrics:
            x_axis_name = ldb.metric_type.iloc[0]
            y_axis_name = ldb["fairness_metric"].iloc[0]
                
            # Scatter plot
            plt.figure(figsize=(10, 7))
            plt.plot(ldb.metric_value, ldb[fm], "*", markersize=12, alpha=0.75)
            plt.xlabel(x_axis_name)
            plt.ylabel(y_axis_name)
            plt.title(f"Performance vs {fm}")
            plt.tight_layout(pad=2.0)
            fname = f"performance_vs_{fm}.png"
            plot_path = os.path.join(model_path, fname)
            plt.savefig(plot_path)
            plt.close("all")

            fout.write(f"\n\n### Performance vs {fm}\n")
            fout.write(f"![Performance vs {fm}]({fname})")

