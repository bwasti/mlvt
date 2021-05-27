import mlvt
import numpy as np
import time


def train(iters):
    import math

    with mlvt.Reprint() as rp:
        # black red green yellow blue magenta cyan white
        # bright_black bright_red bright_green bright_yellow
        # bright_blue bright_magenta bright_cyan bright_white
        loss_plot = mlvt.Line(60, 8, accumulate=50, color="cyan")
        w_plot = mlvt.Histogram(32, 8, color="bright_blue")
        g_plot = mlvt.Histogram(32, 8, color="magenta")
        w_viz = mlvt.Heatmap(18, 10, color=("bright_blue", "blue"))
        g_viz = mlvt.Heatmap(18, 10, color=("bright_magenta", "magenta"))
        scroll = mlvt.TextBuffer(100, 10)

        weights = np.random.randn(100, 100)
        grad = np.random.randn(100, 100) * 0.1
        for i in range(iters):
            # simulated training data
            loss = 10 / (math.log(i + 1) + 1)
            weights += grad
            grad = np.random.randn(100, 100) * 0.1

            loss_plot.update(loss)
            w_plot.update(weights.flatten())
            g_plot.update(grad.flatten())
            w_viz.update(weights)
            g_viz.update(grad)
            scroll.update(np.round(np.random.randn(12)))

            print(
                mlvt.horiz_concat(
                    f"loss: {loss}\n\n{loss_plot}",
                    f"examples:\n\n{scroll}",
                    padding=5,
                    center=False,
                )
            )
            print(
                mlvt.horiz_concat(
                    f"weight distrib:\n\n{w_plot}",
                    f"heatmap:\n\n{w_viz}",
                    f"weight distrib:\n\n{w_plot}",
                    f"heatmap:\n\n{w_viz}",
                    padding=5,
                )
            )
            print()
            print(
                mlvt.horiz_concat(
                    f"grad distrib:\n\n{g_plot}",
                    f"heatmap:\n\n{g_viz}",
                    f"grad distrib:\n\n{g_plot}",
                    f"heatmap:\n\n{g_viz}",
                    padding=5,
                )
            )

            rp.flush()
            time.sleep(0.1)


if __name__ == "__main__":
    try:
        train(1000)
    except KeyboardInterrupt:
        pass
