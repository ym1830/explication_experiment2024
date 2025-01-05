import random
import pandas as pd

# Define the basic parameters
original_samples = {
    "A": ["A1", "A2", "A3"],
    "B": ["B1", "B2", "B3"],
    "C": ["C1", "C2", "C3"],
    "D": ["D1", "D2", "D3"]
}

num_participants = 45
samples_per_participant = 4
participants_per_group = 15

# Prepare the participant IDs
participant_ids = [f"{i+1:03d}" for i in range(num_participants)]

# Generate the randomized participant distribution
all_participants = []

# Repeat the assignment process 15 times (for 45 participants)
for _ in range(participants_per_group):
    # Create fresh copies of the sample lists and shuffle them
    sample_lists = {group: original_samples[group].copy() for group in original_samples}
    for group in sample_lists:
        random.shuffle(sample_lists[group])

    # Assign samples to 3 participants in each cycle
    for i in range(3):
        selected_samples = [sample_lists[group].pop() for group in sample_lists]
        random.shuffle(selected_samples) # サンプルの順序をランダム化
        order_tags = [str(random.randint(1, 2)) for _ in range(samples_per_participant)]
        participant_id = participant_ids.pop(0)
        full_id = "".join(selected_samples) + "".join(order_tags) + participant_id

        all_participants.append({
            "Participant ID": participant_id,  # 保存したIDを利用
            "Sample Tags": selected_samples,
            "Order Tags": order_tags,
            "Full ID": full_id
        })



# Create a DataFrame to visualize the distribution
df = pd.DataFrame(all_participants)
df.to_csv("randomized_participant_assignment.csv", index=False)

# Verify distribution consistency
sample_counts = {sample: 0 for group in original_samples for sample in original_samples[group]}
for participant in all_participants:
    for sample in participant["Sample Tags"]:
        sample_counts[sample] += 1

assert all(count == 15 for count in sample_counts.values()), "Some samples did not reach 15 assignments!"
