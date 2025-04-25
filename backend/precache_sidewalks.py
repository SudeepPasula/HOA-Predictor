import pandas as pd
from feature_extractor import check_sidewalk_nearby
from tqdm import tqdm

# === CONFIGURATION === #
CSV_PATH = "hoa_training.csv"
OUTPUT_PATH = "hoa_training_sampled.csv"
SAMPLE_SIZE = 2000

# === LOAD & SAMPLE DATA === #
df = pd.read_csv(CSV_PATH)
df_sample = df.sample(n=SAMPLE_SIZE, random_state=42).copy()

print(f"📊 Sampled {SAMPLE_SIZE} rows from full dataset\n")

# === ADD SIDEWALK PRESENCE === #
tqdm.pandas()
df_sample["has_sidewalk"] = df_sample.progress_apply(
    lambda row: check_sidewalk_nearby(row.latitude, row.longitude), axis=1
)

# === SAVE OUTPUT === #
df_sample.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Sidewalk-enriched sample saved to {OUTPUT_PATH}")
