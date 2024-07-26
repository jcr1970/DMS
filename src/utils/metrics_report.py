# src/utils/metrics_report.py

import matplotlib.pyplot as plt
import json

def generate_metrics_report(engagement_data, total_time, frame_count):
    frame_time = total_time / frame_count

    # Calculate total time and percentages
    total_engagement_time = {stimulus: count * frame_time for stimulus, count in engagement_data.items()}
    total_engagement = sum(total_engagement_time.values())
    engagement_percentage = {stimulus: (time / total_engagement) * 100 for stimulus, time in total_engagement_time.items()}

    # Calculate engagement scores
    engagement_score = 100
    for stimulus, time in total_engagement_time.items():
        if stimulus != 'road':
            engagement_score -= (time / total_time) * 100
            if time > 5:  # Example rule: if time on non-road stimuli exceeds 5 seconds consecutively, decrease score
                engagement_score -= (time - 5) / total_time * 100
    engagement_score = max(engagement_score, 0)

    # Find most and least engaged stimuli
    most_engaged_stimulus = max(engagement_percentage, key=engagement_percentage.get)
    least_engaged_stimulus = min(engagement_percentage, key=engagement_percentage.get)

    # Save data to a JSON file for use by Streamlit
    report_data = {
        'engagement_percentage': engagement_percentage,
        'total_time': total_time,
        'engagement_score': engagement_score,
        'most_engaged_stimulus': most_engaged_stimulus,
        'least_engaged_stimulus': least_engaged_stimulus,
        'total_engagement_time': total_engagement_time,
        
    }
    report_file_path = 'src/data/report_data.json'
    with open(report_file_path, 'w') as report_file:
        json.dump(report_data, report_file)

    # Print the metrics report
    print("\nEngagement Metrics Report:")
    print("----------------------------")
    for stimulus, percentage in engagement_percentage.items():
        print(f"{stimulus}: {percentage:.2f}%")
    print(f"\nTotal tracking time: {total_time:.2f} seconds")
    print(f"Engagement score: {engagement_score:.2f}%")
    print(f"Most engaged stimulus: {most_engaged_stimulus} ({engagement_percentage[most_engaged_stimulus]:.2f}%)")
    print(f"Least engaged stimulus: {least_engaged_stimulus} ({engagement_percentage[least_engaged_stimulus]:.2f}%)")

    # Plot vertical bar chart for engagement percentages
    plt.figure(figsize=(10, 6))
    plt.bar(engagement_percentage.keys(), engagement_percentage.values(), color='skyblue')
    plt.xlabel('Stimuli')
    plt.ylabel('Engagement Percentage')
    plt.title('Engagement Percentage by Stimuli')
    plt.tight_layout()
    plt.savefig('src/data/engagement_percentage.png')
    plt.close()

    # Plot horizontal bar chart for total engagement time
    plt.figure(figsize=(10, 6))
    plt.barh(list(total_engagement_time.keys()), list(total_engagement_time.values()), color='lightgreen')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Stimuli')
    plt.title('Total Engagement Time by Stimuli')
    plt.tight_layout()
    plt.savefig('src/data/engagement_time.png')
    plt.close()
