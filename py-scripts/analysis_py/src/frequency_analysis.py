#!/usr/bin/env python3
"""
Script to parse Vivado analysis log files and plot target frequency vs achieved frequency.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from parsers import parse_achieved_frequencies
from plotter import setup_plot_style


def plot_target_vs_achieved_frequency(file_path, output_path=None, show_plot=True):
    """
    Parse a Vivado analysis log file and create a plot of target vs achieved frequency.
    
    Args:
        file_path (str): Path to the Vivado log file
        output_path (str, optional): Path to save the plot. If None, shows the plot instead.
        show_plot (bool): Whether to display the plot interactively
    """
    # Parse the frequencies from the log file
    target_frequencies, achieved_frequencies = parse_achieved_frequencies(file_path)
    
    if not target_frequencies or not achieved_frequencies:
        print(f"Error: No frequency data found in {file_path}")
        return
    
    # Set up plot style
    # setup_plot_style(font_size=14, figsize=(25, 12))
    
    # Create the plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 16))
    
    # Plot target vs achieved frequency
    ax.plot(target_frequencies, achieved_frequencies, 
            'o-', color='royalblue', linewidth=2, markersize=8, 
            label='Achieved Frequency')
    
    # Add perfect performance line (45-degree line where target = achieved)
    min_freq = min(min(target_frequencies), min(achieved_frequencies))
    max_freq = max(max(target_frequencies), max(achieved_frequencies))
    # ax.plot([min_freq, max_freq], [min_freq, max_freq], 
    #         '--', color='red', linewidth=2, alpha=0.7, 
    #         label='Perfect Performance (Target = Achieved)')
    
    # Customize the plot
    ax.set_xlabel('Target Frequency (MHz)', fontsize=16)
    ax.set_ylabel('Achieved Frequency (MHz)', fontsize=16)
    ax.set_title('Target vs Achieved Frequency Analysis', fontsize=18)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12)
    
    # Make axes equal and set reasonable limits
    ax.set_aspect('equal')
    margin = (max_freq - min_freq) * 0.05
    ax.set_xlim(min_freq - margin, max_freq + margin)
    ax.set_ylim(min_freq - margin, max_freq + margin)
    
    # Add statistics text box
    avg_target = np.mean(target_frequencies)
    avg_achieved = np.mean(achieved_frequencies)
    max_achieved = max(achieved_frequencies)
    min_achieved = min(achieved_frequencies)
    
    # stats_text = f"""Statistics:
    # Avg Target: {avg_target:.1f} MHz
    # Avg Achieved: {avg_achieved:.1f} MHz
    # Max Achieved: {max_achieved:.1f} MHz
    # Min Achieved: {min_achieved:.1f} MHz"""
    
    # ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
    #         verticalalignment='top', bbox=dict(boxstyle='round', 
    #         facecolor='white', alpha=0.8), fontsize=10)
    
    plt.tight_layout()
    
    # Save or show the plot
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {output_path}")
    
    if show_plot:
        plt.show()
    else:
        plt.close()


def main():
    """
    Main function to handle command line arguments and run the analysis.
    """
    if len(sys.argv) < 2:
        print("Usage: python frequency_analysis.py <log_file_path> [output_path]")
        print("Example: python frequency_analysis.py vivado_analysis_on_queue_size_3.txt")
        print("Example: python frequency_analysis.py vivado_analysis_on_queue_size_3.txt freq_plot.png")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if file exists
    if not os.path.exists(log_file_path):
        print(f"Error: File {log_file_path} not found!")
        sys.exit(1)
    
    # Run the analysis
    plot_target_vs_achieved_frequency(log_file_path, output_path, show_plot=(output_path is None))


if __name__ == "__main__":
    main() 