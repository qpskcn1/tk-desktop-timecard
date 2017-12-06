import os
import sys
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
# sgtk.util.append_path_to_env_var("PYTHONPATH", startup_path)

from datetime import datetime, timedelta

# from aw_core.transforms import filter_period_intersect, filter_keyvals
# import aw_client

# client = aw_client.ActivityWatchClient()
# starttime = datetime.now().replace(hour=0, minute=0)

# windowevents = client.get_events("aw-watcher-window_OFG-TESTBENCH", start=starttime)
# chrome_events = filter_keyvals(windowevents, "app", ["sublime_text.exe"])

# afkevents = client.get_events("aw-watcher-afk_OFG-TESTBENCH", start=starttime)
# afkevents_filtered = filter_keyvals(afkevents, "status", ["not-afk"])

# chrome_events_filtered = filter_period_intersect(windowevents, afkevents_filtered)

# print chrome_events_filtered

from aw_core.transforms import full_chunk, filter_keyvals
import aw_client

client = aw_client.ActivityWatchClient()
starttime = datetime.now().replace(hour=0, minute=0)

windowevents = client.get_events("aw-watcher-window_OFG-TESTBENCH", start=starttime, limit=-1)
nuke_events = filter_keyvals(windowevents, "app", ["Nuke10.5.exe"])
chunk_result = full_chunk(nuke_events, "title", False)
chunks = chunk_result.chunks
def chunkDuration(chunk):
	return chunks[chunk]['duration']

# pprint(sorted(chunks, key=chunkDuration, reverse=True))
pprint(chunks)
# pprint(nuke_events)