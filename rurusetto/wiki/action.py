"""File that contain all action command that can run from web interface."""

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .function import source_link_type
from .models import RecommendBeatmap, Ruleset, RulesetStatus
from rurusetto.settings import OSU_API_V1_KEY, GITHUB_TOKEN
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import requests
import os
import time
from dateutil import parser


def update_all_beatmap_action(action):
    """
    Action to update all RecommendBeatmap object in the database by fetching and replace with new
    data from osu! API one by one.

    Action area : maintainer

    :param action: Action model object that contain and update the log to the view
    """
    # Check all beatmaps number that the worker need to run
    beatmap_number = RecommendBeatmap.objects.all().count()
    failed = 0
    success = 0
    count = 0
    action.save()
    # Update each beatmap to new data one by one
    for beatmap in RecommendBeatmap.objects.all():
        count += 1
        action.running_text = f"Updating {beatmap.title} [{beatmap.version}] ({count}/{beatmap_number})"
        action.save()
        parameter = {'b': int(beatmap.beatmap_id), 'm': 0, 'k': OSU_API_V1_KEY}
        request_data = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=parameter)
        if (request_data.status_code == 200) and (request_data.json() != []):
            try:
                beatmap_json_data = request_data.json()[0]

                action.running_text = f"Fetching the new cover of {beatmap.title} [{beatmap.version}] ({count}/{beatmap_number})"
                action.save()

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

                action.running_text = f"Fetching the new thumbnail of {beatmap.title} [{beatmap.version}] ({count}/{beatmap_number})"
                action.save()

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

                action.running_text = f"Updating all metadata of {beatmap.title} [{beatmap.version}] ({count}/{beatmap_number})"
                action.save()

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
            except ObjectDoesNotExist:
                failed += 1
        else:
            failed += 1
        # Need to add sleep to make the API fetching not to rush
        time.sleep(5)
    # After task successfully, update Action log to success and update finish time.
    action.status = 2
    action.running_text = f"Task running successfully with {success} success and {failed} failed!"
    action.time_finish = timezone.now()
    action.save()


def update_ruleset_version_action(action):
    """
    Action to update the RulesetStatus of Ruleset object that has GitHub link as the source.

    Action area : maintainer

    :param action: Action model object that contain and update the log to the view
    """
    failed = 0
    success = 0
    skip = 0
    update_count = 0
    progress_round = 0
    # 1440 round to make it run for full 3 days
    for round_count in range(100):
        progress_round += 1
        action.status = 1
        action.running_text = f"Start a new round (Round {progress_round}/1440)"
        action.save()
        for ruleset_status in RulesetStatus.objects.all():
            action.running_text = f"Updating {ruleset_status.ruleset.name} (Round {progress_round}/1440)"
            action.save()
            if source_link_type(ruleset_status.ruleset.source) == "github":
                try:
                    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                    request_data = requests.get("https://api.github.com/repos/ppy/osu/releases/latest", headers=headers).json()

                    ruleset_status.latest_version = request_data['name']
                    ruleset_status.latest_update = timezone.localtime(parser.parse(request_data['published_at']))
                    ruleset_status.changelog = request_data['body']

                    all_assets = request_data['assets']

                    for assets in all_assets:
                        if assets["name"] == ruleset_status.ruleset.github_download_filename:
                            ruleset_status.file_size = request_data['assets']
                            continue

                    ruleset_status.save()
                    success += 1
                    update_count += 1
                except KeyError:
                    failed += 1
                    update_count += 1
            else:
                skip += 1
                update_count += 1
        # Sleep to make it update every 3 minutes
        action.status = 0
        action.running_text = f"Wait for countdown (Round {progress_round}/1440)"
        action.save()
        time.sleep(180)
    # After task successfully, update Action log to success and update finish time.
    action.status = 2
    action.running_text = f"Task running successfully with {success} success ,{failed} failed, {skip} skipped with {update_count} updated and {progress_round} round"
    action.time_finish = timezone.now()
    action.save()


