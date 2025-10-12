import matplotlib

matplotlib.use("TkAgg")

import pandas as pd
import matplotlib.pyplot as plt
import os
import glob


def plot_average_graph_all(mode, step=50000, smooth_window=5):
    """
    Plots the average match time across all CSV files of a given mode.

    Parameters:
        mode (str): The mode to plot (e.g., 'kmp').
        step (int): Number of rows to average over.
        smooth_window (int): Window size for rolling average smoothing.
    """
    folder_path = f"TestResultsLines/{mode}/"
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))

    if not all_files:
        print(f"No CSV files found in {folder_path}")
        return

    print(f"Found {len(all_files)} CSV files. Combining...")

    # Read and concatenate all CSVs
    df_list = [pd.read_csv(file) for file in all_files]
    df = pd.concat(df_list, ignore_index=True)

    # Sort by Units Processed to ensure monotonic x-axis
    df = df.sort_values("Units Processed").reset_index(drop=True)

    # Group and average
    df["group"] = df.index // step
    df_avg = df.groupby("group", as_index=False).agg({
        "Units Processed": "max",
        "Time (s)": "mean"
    })

    # Apply rolling average for smoothing
    df_avg["Time (s) Smoothed"] = df_avg["Time (s)"].rolling(
        window=smooth_window,
        center=True,
        min_periods=1
    ).mean()

    # Plot
    plt.figure(figsize=(14, 6))
    plt.plot(df_avg["Units Processed"], df_avg["Time (s)"],
             linewidth=2, color='lightblue', alpha=0.8, label='Raw Average', marker='o', markersize=2)
    plt.plot(df_avg["Units Processed"], df_avg["Time (s) Smoothed"],
             linewidth=2.5, color='darkblue', label=f'Smoothed (window={smooth_window})')
    plt.title(f"Average Match Time Across All {mode.upper()} Searches")
    plt.xlabel("Units Processed")
    plt.ylabel("Average Time (s)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    # Create graphs directory if it doesn't exist
    os.makedirs("graphs", exist_ok=True)

    # Save the figure
    output_filename = f"graphs/average_performance_{mode}_{step}_{smooth_window}.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Graph saved as: {output_filename}")

    plt.show()

    print(f"Total rows combined: {len(df)}")
    print(f"Average time: {df['Time (s)'].mean():.4f}s")
    print(f"Grouped into {len(df_avg)} bins with step={step}")


def plot_comparison_all_modes(modes=['kmp', 'boyer', 'regex'], step=50000, smooth_window=5):
    """
    Plots smoothed average match time comparison across multiple search modes.

    Parameters:
        modes (list): List of modes to plot (e.g., ['kmp', 'boyer', 'regex']).
        step (int): Number of rows to average over.
        smooth_window (int): Window size for rolling average smoothing.
    """
    plt.figure(figsize=(14, 7))

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Different colors for each mode

    for mode, color in zip(modes, colors):
        folder_path = f"TestResultsLines/{mode}/"
        all_files = glob.glob(os.path.join(folder_path, "*.csv"))

        if not all_files:
            print(f"No CSV files found in {folder_path}")
            continue

        print(f"Processing {mode.upper()}... Found {len(all_files)} CSV files.")

        # Read and concatenate all CSVs
        df_list = [pd.read_csv(file) for file in all_files]
        df = pd.concat(df_list, ignore_index=True)

        # Sort by Units Processed to ensure monotonic x-axis
        df = df.sort_values("Units Processed").reset_index(drop=True)

        # Group and average
        df["group"] = df.index // step
        df_avg = df.groupby("group", as_index=False).agg({
            "Units Processed": "max",
            "Time (s)": "mean"
        })

        # Apply rolling average for smoothing
        df_avg["Time (s) Smoothed"] = df_avg["Time (s)"].rolling(
            window=smooth_window,
            center=True,
            min_periods=1
        ).mean()

        # Plot smoothed line only
        plt.plot(df_avg["Units Processed"], df_avg["Time (s) Smoothed"],
                 linewidth=2.5, color=color, label=f'{mode.upper()} (avg: {df["Time (s)"].mean():.4f}s)', marker='o',
                 markersize=3)

        print(f"{mode.upper()}: Average time = {df['Time (s)'].mean():.4f}s, {len(df_avg)} bins")

    plt.title("Search Algorithm Performance Comparison (Smoothed)", fontsize=14, fontweight='bold')
    plt.xlabel("Units Processed", fontsize=12)
    plt.ylabel("Average Time (s)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()

    # Create graphs directory if it doesn't exist
    os.makedirs("graphs", exist_ok=True)

    # Save the figure
    output_filename = f"graphs/comparison_all_modes_{step}_{smooth_window}.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"\nComparison graph saved as: {output_filename}")

    plt.show()

# Example usage - try these step sizes
#plot_average_graph_all("regex", step=30000, smooth_window=5)

# Compare all three modes
plot_comparison_all_modes(modes=['kmp', 'boyer', 'regex'], step=30000, smooth_window=5)