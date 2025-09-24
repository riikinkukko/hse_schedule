import asyncio
import hashlib
import requests
import pandas as pd
from io import StringIO


class SchedulePinger:
    def __init__(self, spreadsheet_id: str, gid: int = 0):
        self.spreadsheet_id = spreadsheet_id
        self.gid = gid
        self.url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
        self.last_hash = None

    def fetch_schedule(self) -> pd.DataFrame:
        response = requests.get(self.url, timeout=15)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df
    
    def get_hash(self, df: pd.DataFrame) -> str:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        return hashlib.md5(csv_bytes).hexdigest()
    
    def has_changed(self) -> bool:
        df = self.fetch_schedule()
        new_hash = self.get_hash(df)

        if self.last_hash is None:
            self.last_hash = new_hash
            return False  

        if new_hash != self.last_hash:
            self.last_hash = new_hash
            return True

        return False
    
    async def run_loop(self, interval: int = 3600 * 5):
        while True:
            try:
                changed = self.has_changed()
                if changed:
                    print("Something")
                else:
                    print("Nothing changed")
            except Exception as e:
                print(e)
        await asyncio.sleep(interval)



if __name__ == "__main__":
    pinger = SchedulePinger(spreadsheet_id="1kAW6IYJkMbpfwPCM1lO4if0NHECPZWK2VEUGnfFgSAs",
                            gid=850497792)
    asyncio.run(pinger.run_loop())
