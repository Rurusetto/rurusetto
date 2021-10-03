from .models import RecommendBeatmap
from rurusetto.settings import OSU_API_V1_KEY
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import requests
import os


def update_all_beatmap_action(action):
    # Check all beatmaps number that the worker need to run
    beatmap_number = RecommendBeatmap.objects.all().count()
    failed = 0
    success = 0
    count = 0
    action.save()
    for beatmap in RecommendBeatmap.objects.all():
        count += 1
        action.running_text = f"Updating {beatmap.title}[{beatmap.version}] ({count}/{beatmap_number})"
        action.save()
        parameter = {'b': int(beatmap.beatmap_id), 'm': 0, 'k': OSU_API_V1_KEY}
        request_data = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=parameter)
        if (request_data.status_code == 200) and (request_data.json() != []):
            try:
                beatmap_json_data = request_data.json()[0]

                # Try to delete old cover picture, if failed just pass it.
                try:
                    os.remove(f"media/{beatmap.beatmap_cover}")
                except FileNotFoundError:
                    pass

                cover_pic = requests.get(
                    f"https://assets.ppy.sh/beatmaps/{beatmap_json_data['beatmapset_id']}/covers/cover.jpg")
                cover_temp = NamedTemporaryFile(delete=True)
                cover_temp.write(cover_pic.content)
                cover_temp.flush()
                beatmap.beatmap_cover.save(f"{beatmap.beatmap_id}.jpg", File(cover_temp), save=True)

                # Try to delete old cover picture, if failed just pass it.
                try:
                    os.remove(f"media/{beatmap.beatmap_thumbnail}")
                except FileNotFoundError:
                    pass

                thumbnail_pic = requests.get(
                    f"https://b.ppy.sh/thumb/{beatmap_json_data['beatmapset_id']}l.jpg")
                thumbnail_temp = NamedTemporaryFile(delete=True)
                thumbnail_temp.write(thumbnail_pic.content)
                thumbnail_temp.flush()
                beatmap.beatmap_thumbnail.save(f"{beatmap.beatmap_id}.jpg", File(thumbnail_temp), save=True)

                beatmap.beatmapset_id = beatmap_json_data['beatmapset_id']
                beatmap.title = beatmap_json_data['title']
                beatmap.artist = beatmap_json_data['artist']
                beatmap.source = beatmap_json_data['source']
                beatmap.creator = beatmap_json_data['creator']
                beatmap.approved = beatmap_json_data['approved']
                beatmap.difficultyrating = beatmap_json_data['difficultyrating']
                beatmap.bpm = beatmap_json_data['bpm']
                beatmap.version = beatmap_json_data['version']
                beatmap.url = f"https://osu.ppy.sh/beatmapsets/{beatmap_json_data['beatmapset_id']}#osu/{beatmap.beatmap_id}"
                beatmap.save()
                success += 1
            except:
                failed += 1
        else:
            failed += 1
    action.status = 2
    action.running_text = f"Task running successfully with {success} success and {success} failed!"
    action.save()
