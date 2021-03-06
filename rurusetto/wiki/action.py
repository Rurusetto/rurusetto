"""File that contain all action command that can run from web interface."""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import datetime
from .function import source_link_type
from .models import RecommendBeatmap, Ruleset, RulesetStatus
from rurusetto.settings import OSU_API_V1_KEY, GITHUB_TOKEN
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.utils.timezone import make_aware
from django.utils import timezone
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

                action.running_text = f"Fetching the new card of {beatmap.title} [{beatmap.version}] ({count}/{beatmap_number})"
                action.save()

                # Try to delete old card picture, if failed just pass it.
                try:
                    os.remove(f"media/{beatmap.beatmap_card}")
                except FileNotFoundError:
                    pass

                # Download beatmap card to beatmap_card field
                card_pic = requests.get(
                    f"https://assets.ppy.sh/beatmaps/{beatmap_json_data['beatmapset_id']}/covers/card.jpg")
                card_temp = NamedTemporaryFile(delete=True)
                card_temp.write(card_pic.content)
                card_temp.flush()
                beatmap.beatmap_card.save(f"{beatmap.beatmap_id}.jpg", File(card_temp), save=True)

                action.running_text = f"Fetching the new thumbnail of {beatmap.title} [{beatmap.version}] ({count}/{beatmap_number})"
                action.save()

                # Try to delete old list picture, if failed just pass it.
                try:
                    os.remove(f"media/{beatmap.beatmap_list}")
                except FileNotFoundError:
                    pass

                # Download beatmap list picture to beatmap_list field
                list_pic = requests.get(
                    f"https://assets.ppy.sh/beatmaps/{beatmap_json_data['beatmapset_id']}/covers/list.jpg")
                list_temp = NamedTemporaryFile(delete=True)
                list_temp.write(list_pic.content)
                list_temp.flush()
                beatmap.beatmap_list.save(f"{beatmap.beatmap_id}.jpg", File(list_temp), save=True)

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
                beatmap.playcount = beatmap_json_data['playcount']
                beatmap.favourite_count = beatmap_json_data['favourite_count']
                beatmap.total_length = beatmap_json_data['total_length']
                beatmap.creator_id = beatmap_json_data['creator_id']
                beatmap.genre_id = beatmap_json_data['genre_id']
                beatmap.language_id = beatmap_json_data['language_id']
                beatmap.tags = beatmap_json_data['tags']
                beatmap.submit_date = make_aware(
                    datetime.datetime.strptime(beatmap_json_data['submit_date'], '%Y-%m-%d %H:%M:%S'))
                if beatmap_json_data['approved_date'] is not None:
                    beatmap.approved_date = make_aware(
                        datetime.datetime.strptime(beatmap_json_data['approved_date'], '%Y-%m-%d %H:%M:%S'))
                beatmap.last_update = make_aware(
                    datetime.datetime.strptime(beatmap_json_data['last_update'], '%Y-%m-%d %H:%M:%S'))
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
    for round_count in range(1440):
        progress_round += 1
        action.status = 1
        action.running_text = f"Start a new round (Round {progress_round}/1440)"
        action.save()
        for ruleset_status in RulesetStatus.objects.all():
            action.running_text = f"Updating {ruleset_status.ruleset.name} (Round {progress_round}/1440)"
            action.save()
            if source_link_type(ruleset_status.ruleset.source) == "github" and ruleset_status.ruleset.github_download_filename != "":
                try:
                    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                    split_github_link = ruleset_status.ruleset.source.split("/")
                    # If the GitHub link is right when split with slash it must slice to 6 pieces (with slash
                    # at the end) or 5 (without slash at the end)
                    if len(split_github_link) == 6 or len(split_github_link) == 5:
                        if ruleset_status.pre_release:
                            request_data = requests.get(
                                f"https://api.github.com/repos/{split_github_link[3]}/{split_github_link[4]}/releases",
                                headers=headers).json()[0]
                        else:
                            request_data = requests.get(
                                f"https://api.github.com/repos/{split_github_link[3]}/{split_github_link[4]}/releases/latest",
                                headers=headers).json()
                    else:
                        continue

                    ruleset_status.latest_version = request_data['name']
                    ruleset_status.latest_update = timezone.localtime(parser.parse(request_data['published_at']))
                    ruleset_status.changelog = request_data['body']

                    all_assets = request_data['assets']

                    for assets in all_assets:
                        if assets["name"] == ruleset_status.ruleset.github_download_filename:
                            ruleset_status.file_size = assets['size']
                            break

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
        time.sleep(900)
    # After task successfully, update Action log to success and update finish time.
    action.status = 2
    action.running_text = f"Task running successfully with {success} success ,{failed} failed, {skip} skipped with {update_count} updated and {progress_round} round"
    action.time_finish = timezone.now()
    action.save()


def update_ruleset_version_once_action(action):
    """
    Action to update the RulesetStatus of Ruleset object that has GitHub link as the source only one time.

    This will run by maintainer when the update_ruleset_version_action is not working or
    some accident happen.

    Action area : maintainer

    :param action: Action model object that contain and update the log to the view
    """
    total = RulesetStatus.objects.all().count()
    failed = 0
    success = 0
    skip = 0
    update_count = 0
    action.status = 1
    action.save()
    for ruleset_status in RulesetStatus.objects.all():
        update_count += 1
        action.running_text = f"Updating {ruleset_status.ruleset.name} ({update_count}/{total})"
        action.save()
        if source_link_type(
                ruleset_status.ruleset.source) == "github" and ruleset_status.ruleset.github_download_filename != "":
            try:
                headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                split_github_link = ruleset_status.ruleset.source.split("/")
                # If the GitHub link is right when split with slash it must slice to 6 pieces (with slash
                # at the end) or 5 (without slash at the end)
                if len(split_github_link) == 6 or len(split_github_link) == 5:
                    if ruleset_status.pre_release:
                        request_data = requests.get(
                            f"https://api.github.com/repos/{split_github_link[3]}/{split_github_link[4]}/releases",
                            headers=headers).json()[0]
                    else:
                        request_data = requests.get(
                            f"https://api.github.com/repos/{split_github_link[3]}/{split_github_link[4]}/releases/latest",
                            headers=headers).json()
                else:
                    continue

                ruleset_status.latest_version = request_data['name']
                ruleset_status.latest_update = timezone.localtime(parser.parse(request_data['published_at']))
                ruleset_status.changelog = request_data['body']

                all_assets = request_data['assets']

                for assets in all_assets:
                    if assets["name"] == ruleset_status.ruleset.github_download_filename:
                        ruleset_status.file_size = assets['size']
                        break

                ruleset_status.save()
                success += 1
            except KeyError:
                failed += 1
        else:
            skip += 1
    # After task successfully, update Action log to success and update finish time.
    action.status = 2
    action.running_text = f"Task running successfully with {success} success ,{failed} failed, {skip} skipped!"
    action.time_finish = timezone.now()
    action.save()