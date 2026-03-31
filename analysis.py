import pandas as pd

def load_csv(path):
    return pd.read_csv(path, quotechar='"', on_bad_lines='skip')

# Load data
df_fb = load_csv("data/facebook_data.csv")
df_ig = load_csv("data/instagram_data.csv")
df_li = load_csv("data/linkedin_data.csv")

# Add platform
df_fb["platform"] = "Facebook"
df_ig["platform"] = "Instagram"
df_li["platform"] = "LinkedIn"

# Merge
df = pd.concat([df_fb, df_ig, df_li], ignore_index=True)

# Engagement
df["engagement"] = df["likes"] + df["comments"] + df["shares"]

# Time format
df["created_time"] = pd.to_datetime(df["created_time"])

print("\n🔥 TOP POSTS:")
print(df.sort_values("engagement", ascending=False).head())

print("\n📊 PLATFORM AVERAGE ENGAGEMENT:")
print(df.groupby("platform")["engagement"].mean())

print("\n📈 TOTAL ENGAGEMENT:")
print(df.groupby("platform")["engagement"].sum())