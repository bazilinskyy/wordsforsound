from app import db, models, views
from datetime import datetime
import shutil, os

#
try:
	shutil.rmtree('db_repository')
except:
	pass
try:
	os.remove('app.db')
except:
	pass

import db_create

# Add tags
tag_beep = models.Tag(name="beep")
tag_honk = models.Tag(name="honk")
tag_urgent1= models.Tag(name="urgent-1")
tag_urgent2 = models.Tag(name="urgent-2")
tag_urgent3 = models.Tag(name="urgent-3")
tag_urgent4 = models.Tag(name="urgent-4")
tag_looming = models.Tag(name="looming")
tag_spatial= models.Tag(name="spatial")
tag_spoken = models.Tag(name="spoken")
tag_female = models.Tag(name="female")
tag_male = models.Tag(name="male")
tag_short = models.Tag(name="short")
tag_long = models.Tag(name="long")
tag_sharp = models.Tag(name="sharp")
tag_tor = models.Tag(name="take-over request")
tag_fast = models.Tag(name="fast")
tag_precise = models.Tag(name="precise")
tag_unprecise = models.Tag(name="unprecise")
tag_reverb = models.Tag(name="reverb")
tag_volumnious = models.Tag(name="voluminous")
tag_trash = models.Tag(name="trash")
tag_slurred = models.Tag(name="slurred")
tag_nice = models.Tag(name="nice")
tag_positive = models.Tag(name="positive")
tag_negative = models.Tag(name="negative")
tag_wave = models.Tag(name="wave")
tag_acknowledge = models.Tag(name="acknowledge")
tag_playful = models.Tag(name="playful")
tag_fussy = models.Tag(name="fussy")
tag_starting = models.Tag(name="starting")
tag_informative = models.Tag(name="informative")
tag_clear = models.Tag(name="clear")
tag_unclear = models.Tag(name="unclear")
tag_warning = models.Tag(name="warning")
tag_high = models.Tag(name="high")
tag_low = models.Tag(name="low")
tag_metallic = models.Tag(name="metallic")
tag_wooden = models.Tag(name="wooden")
tag_worthy = models.Tag(name="worthy")
tag_popup = models.Tag(name="popup")
tag_shorter = models.Tag(name="shorter")
tag_hard_to_hear = models.Tag(name="hard to hear")
tag_misleading = models.Tag(name="misleading")
tag_neutral = models.Tag(name="neutral")
tag_wrong = models.Tag(name="wrong")
tag_peaceful = models.Tag(name="peaceful")
tag_nervous = models.Tag(name="nervous")
tag_sport = models.Tag(name="sport")
tag_active = models.Tag(name="active")
tag_movement = models.Tag(name="movement")
tag_computer = models.Tag(name="computer")
tag_opening = models.Tag(name="opening")
tag_notification = models.Tag(name="notification")
tag_sudden = models.Tag(name="sudden")
tag_speed = models.Tag(name="speed")
tag_transition = models.Tag(name="transition")
tag_sad = models.Tag(name="sad")
tag_unusual = models.Tag(name="unusual")
tag_on = models.Tag(name="on")
tag_angry = models.Tag(name="angry")
tag_speech = models.Tag(name="speech")
tag_command = models.Tag(name="command")
tag_sound = models.Tag(name="sound")
tag_beat = models.Tag(name="beat")
tag_jarring = models.Tag(name="jarring")
tag_click = models.Tag(name="click")
tag_windows = models.Tag(name="windows")
tag_higher_at_the_end = models.Tag(name="higher at the end")
tag_close = models.Tag(name="close")
tag_attention = models.Tag(name="attention")
tag_calm = models.Tag(name="calm")
tag_sleep = models.Tag(name="sleep")
tag_aggressive = models.Tag(name="aggressive")
tag_knock = models.Tag(name="knock")
tag_information = models.Tag(name="information")
tag_signal = models.Tag(name="signal")
tag_accelerated = models.Tag(name="accelerated")
tag_pushing = models.Tag(name="pushing")
tag_stone = models.Tag(name="stone")
tag_clapping = models.Tag(name="clapping")
tag_high_pitch = models.Tag(name="high pitch")
tag_strike = models.Tag(name="strike")
tag_happy = models.Tag(name="happy")
tag_violin = models.Tag(name="violin")
tag_blinking = models.Tag(name="blinking")
tag_assistent = models.Tag(name="assistent")
tag_old_telephone = models.Tag(name="old telephone")
tag_big_hall = models.Tag(name="big hall")
tag_login = models.Tag(name="login")
tag_logout = models.Tag(name="logout")
tag_welcome = models.Tag(name="welcome")
tag_start_of_OS = models.Tag(name="start of OS")
tag_bright = models.Tag(name="bright")
tag_mystical = models.Tag(name="mystical")
tag_audiobook = models.Tag(name="audiobook")
tag_hello = models.Tag(name="hello")
tag_stop = models.Tag(name="stop")
tag_steps = models.Tag(name="steps")
tag_faster = models.Tag(name="faster")
tag_something_happens = models.Tag(name="something happens")
tag_strange = models.Tag(name="strange")
tag_instrument = models.Tag(name="instrument")
tag_woodpecker = models.Tag(name="woodpecker")
tag_hurry = models.Tag(name="hurry")
tag_crash = models.Tag(name="crash")
tag_need_to_intervene = models.Tag(name="need to intervene")
tag_shutdown = models.Tag(name="shutdown")
tag_traffic_lights = models.Tag(name="traffic lights")
tag_move = models.Tag(name="move")
tag_selection_in_menu = models.Tag(name="selection in menu")
tag_telephone = models.Tag(name="telephone")
tag_shutdown_of_OS = models.Tag(name="shutdown of OS")
tag_danger = models.Tag(name="danger")
tag_threat = models.Tag(name="threat")
tag_approach = models.Tag(name="approach")
tag_be_aware = models.Tag(name="be aware")
tag_patience = models.Tag(name="patience")
tag_dull = models.Tag(name="dull")
tag_dance = models.Tag(name="dance")
tag_jingle = models.Tag(name="jingle")
tag_sunrise = models.Tag(name="sunrise")
tag_insect = models.Tag(name="insect")
tag_light = models.Tag(name="light")
tag_clear = models.Tag(name="clear")
tag_uncertain = models.Tag(name="uncertain")
tag_unsecure = models.Tag(name="unsecure")
tag_secret = models.Tag(name="secret")
tag_complex = models.Tag(name="complex")
tag_affirmative = models.Tag(name="affirmative")
tag_bird = models.Tag(name="bird")
tag_jazz = models.Tag(name="jazz")
tag_pains = models.Tag(name="pains")
tag_winter = models.Tag(name="winter")
tag_nature = models.Tag(name="nature")
tag_water = models.Tag(name="water")
tag_persecution = models.Tag(name="persecution")
tag_underground = models.Tag(name="underground")
tag_future = models.Tag(name="future")
tag_automated = models.Tag(name="automated")
tag_electronic = models.Tag(name="electronic")
tag_synthetic = models.Tag(name="synthetic")
tag_not_human = models.Tag(name="not human")
tag_rhythm = models.Tag(name="rhythm")
tag_classic = models.Tag(name="classic")
tag_accord = models.Tag(name="accord")
tag_dull = models.Tag(name="dull")
tag_drawing = models.Tag(name="drawing")
tag_demanding = models.Tag(name="demanding")
tag_speed = models.Tag(name="speed")
tag_weather = models.Tag(name="weather")
tag_flash = models.Tag(name="flash")
tag_wakeup = models.Tag(name="wakeup")
tag_cold = models.Tag(name="cold")

db.session.add(tag_beep)
db.session.add(tag_honk)
db.session.add(tag_urgent1)
db.session.add(tag_urgent2)
db.session.add(tag_urgent3)
db.session.add(tag_urgent4)
db.session.add(tag_looming)
db.session.add(tag_spatial)
db.session.add(tag_spoken)
db.session.add(tag_female)
db.session.add(tag_male)
db.session.add(tag_short)
db.session.add(tag_long)
db.session.add(tag_tor)
db.session.add(tag_fast)
db.session.add(tag_precise)
db.session.add(tag_unprecise)
db.session.add(tag_reverb)
db.session.add(tag_volumnious)
db.session.add(tag_trash)
db.session.add(tag_slurred)
db.session.add(tag_nice)
db.session.add(tag_positive)
db.session.add(tag_negative)
db.session.add(tag_wave)
db.session.add(tag_acknowledge)
db.session.add(tag_playful)
db.session.add(tag_fussy)
db.session.add(tag_starting)
db.session.add(tag_informative)
db.session.add(tag_clear)
db.session.add(tag_unclear)
db.session.add(tag_warning)
db.session.add(tag_high)
db.session.add(tag_low)
db.session.add(tag_metallic)
db.session.add(tag_popup)
db.session.add(tag_shorter)
db.session.add(tag_hard_to_hear)
db.session.add(tag_misleading)
db.session.add(tag_neutral)
db.session.add(tag_wrong)
db.session.add(tag_worthy)
db.session.add(tag_wooden)
db.session.add(tag_peaceful)
db.session.add(tag_nervous)
db.session.add(tag_sport)
db.session.add(tag_active)
db.session.add(tag_movement)
db.session.add(tag_computer)
db.session.add(tag_opening)
db.session.add(tag_notification)
db.session.add(tag_sudden)
db.session.add(tag_speed)
db.session.add(tag_transition)
db.session.add(tag_sad)
db.session.add(tag_unusual)
db.session.add(tag_on)
db.session.add(tag_angry)
db.session.add(tag_speech)
db.session.add(tag_command)
db.session.add(tag_sound)
db.session.add(tag_beat)
db.session.add(tag_jarring)
db.session.add(tag_click)
db.session.add(tag_windows)
db.session.add(tag_higher_at_the_end)
db.session.add(tag_close)
db.session.add(tag_attention)
db.session.add(tag_calm)
db.session.add(tag_sleep)
db.session.add(tag_aggressive)
db.session.add(tag_knock)
db.session.add(tag_information)
db.session.add(tag_signal)
db.session.add(tag_accelerated)
db.session.add(tag_pushing)
db.session.add(tag_stone)
db.session.add(tag_clapping)
db.session.add(tag_high_pitch)
db.session.add(tag_strike)
db.session.add(tag_happy)
db.session.add(tag_violin)
db.session.add(tag_blinking)
db.session.add(tag_assistent)
db.session.add(tag_old_telephone)
db.session.add(tag_big_hall)
db.session.add(tag_login)
db.session.add(tag_logout)
db.session.add(tag_welcome)
db.session.add(tag_start_of_OS)
db.session.add(tag_bright)
db.session.add(tag_mystical)
db.session.add(tag_audiobook)
db.session.add(tag_hello)
db.session.add(tag_stop)
db.session.add(tag_steps)
db.session.add(tag_faster)
db.session.add(tag_something_happens)
db.session.add(tag_strange)
db.session.add(tag_woodpecker)
db.session.add(tag_instrument)
db.session.add(tag_hurry)
db.session.add(tag_crash)
db.session.add(tag_need_to_intervene)
db.session.add(tag_shutdown)
db.session.add(tag_traffic_lights)
db.session.add(tag_move)
db.session.add(tag_selection_in_menu)
db.session.add(tag_telephone)
db.session.add(tag_shutdown_of_OS)
db.session.add(tag_danger)
db.session.add(tag_threat)
db.session.add(tag_approach)
db.session.add(tag_be_aware)
db.session.add(tag_patience)
db.session.add(tag_dull)
db.session.add(tag_dance)
db.session.add(tag_jingle)
db.session.add(tag_sunrise)
db.session.add(tag_light)
db.session.add(tag_clear)
db.session.add(tag_uncertain)
db.session.add(tag_unsecure)
db.session.add(tag_secret)
db.session.add(tag_complex)
db.session.add(tag_affirmative)
db.session.add(tag_bird)
db.session.add(tag_jazz)
db.session.add(tag_pains)
db.session.add(tag_winter)
db.session.add(tag_nature)
db.session.add(tag_water)
db.session.add(tag_persecution)
db.session.add(tag_underground)
db.session.add(tag_future)
db.session.add(tag_automated)
db.session.add(tag_electronic)
db.session.add(tag_synthetic)
db.session.add(tag_not_human)
db.session.add(tag_rhythm)
db.session.add(tag_classic)
db.session.add(tag_accord)
db.session.add(tag_dull)
db.session.add(tag_drawing)
db.session.add(tag_demanding)
db.session.add(tag_speed)
db.session.add(tag_weather)
db.session.add(tag_flash)
db.session.add(tag_wakeup)
db.session.add(tag_cold)

db.session.commit()

# Add custom sounds
sound_beep_freezman = models.Sound(name="Beep freezman",
			filename="22.wav",
			rights="CC Attribution License")
sound_beep_freezman.tag_add(tag_beep)
sound_beep_freezman.tag_add(tag_urgent2)
sound_beep_freezman.tag_add(tag_long)
sound_beep_freezman.tag_add(tag_worthy)
db.session.add(sound_beep_freezman)

# Add sounds from projects
sound_a1 = models.Sound(name="A_1",
			filename="1.wav")
sound_a1.tag_add(tag_speech)
sound_a1.tag_add(tag_female)
sound_a1.tag_add(tag_urgent1)
sound_a1.tag_add(tag_command)
sound_a11 = models.Sound(name="A_11",
			filename="2.wav")
sound_a11.tag_add(tag_short)
sound_a11.tag_add(tag_beep)
sound_a11.tag_add(tag_sound)
sound_a11.tag_add(tag_violin)
sound_a11.tag_add(tag_danger)
sound_a11.tag_add(tag_threat)
sound_a18 = models.Sound(name="A_18",
			filename="3.wav")
sound_a18.tag_add(tag_beat)
sound_a18.tag_add(tag_metallic)
sound_a18.tag_add(tag_long)
sound_a18.tag_add(tag_blinking)
sound_a18.tag_add(tag_traffic_lights)
sound_a18.tag_add(tag_assistent)
sound_a18.tag_add(tag_approach)
sound_a23 = models.Sound(name="A_23",
			filename="4.wav")
sound_a23.tag_add(tag_beep)
sound_a23.tag_add(tag_jarring)
sound_a23.tag_add(tag_short)
sound_a23.tag_add(tag_old_telephone)
sound_a23.tag_add(tag_metallic)
sound_a23.tag_add(tag_cold)
sound_a23.tag_add(tag_big_hall)
sound_a23.tag_add(tag_telephone)
sound_a23.tag_add(tag_be_aware)
sound_a7 = models.Sound(name="A_7",
			filename="5.wav")
sound_a7.tag_add(tag_short)
sound_a7.tag_add(tag_beep)
sound_a7.tag_add(tag_click)
sound_a7.tag_add(tag_windows)
sound_a7.tag_add(tag_login)
sound_a7.tag_add(tag_logout)
sound_a7.tag_add(tag_patience)
sound_a7.tag_add(tag_dull)
sound_a7.tag_add(tag_dance)
sound_a8 = models.Sound(name="A_8",
			filename="6.wav")
sound_a8.tag_add(tag_higher_at_the_end)
sound_a8.tag_add(tag_hello)
sound_a8.tag_add(tag_welcome)
sound_a8.tag_add(tag_start_of_OS)
sound_a8.tag_add(tag_jingle)
sound_a8.tag_add(tag_sunrise)
sound_ad_deactivation = models.Sound(name="AD Deactivation",
			filename="7.wav")
sound_ad_deactivation.tag_add(tag_short)
sound_ad_deactivation.tag_add(tag_close)
sound_ad_deactivation.tag_add(tag_login)
sound_ad_deactivation.tag_add(tag_logout)
sound_ad_deactivation.tag_add(tag_insect)
sound_ad_deactivation.tag_add(tag_light)
sound_ad_notification = models.Sound(name="AD Notification advice",
			filename="8.wav")
sound_ad_notification.tag_add(tag_short)
sound_ad_notification.tag_add(tag_attention)
sound_ad_notification.tag_add(tag_login)
sound_ad_notification.tag_add(tag_logout)
sound_ad_notification.tag_add(tag_bright)
sound_ad_notification.tag_add(tag_clear)
sound_ad_notification.tag_add(tag_precise)
sound_b23 = models.Sound(name="B_23",
			filename="9.wav")
sound_b23.tag_add(tag_long)
sound_b23.tag_add(tag_calm)
sound_b23.tag_add(tag_sleep)
sound_b23.tag_add(tag_mystical)
sound_b23.tag_add(tag_audiobook)
sound_b23.tag_add(tag_uncertain)
sound_b23.tag_add(tag_unsecure)
sound_b23.tag_add(tag_secret)
sound_b25 = models.Sound(name="B_25",
			filename="10.wav")
sound_b25.tag_add(tag_beep)
sound_b25.tag_add(tag_short)
sound_b25.tag_add(tag_login)
sound_b25.tag_add(tag_logout)
sound_b25.tag_add(tag_bright)
sound_b25.tag_add(tag_fast)
sound_b3 = models.Sound(name="B_3",
			filename="11.mp3")
sound_b3.tag_add(tag_aggressive)
sound_b3.tag_add(tag_hello)
sound_b3.tag_add(tag_welcome)
sound_b3.tag_add(tag_complex)
sound_b3.tag_add(tag_affirmative)
sound_b7 = models.Sound(name="B_7",
			filename="12.wav")
sound_b7.tag_add(tag_knock)
sound_b7.tag_add(tag_short)
sound_b7.tag_add(tag_click)
sound_b7.tag_add(tag_woodpecker)
sound_b7.tag_add(tag_bird)
sound_cc_activated = models.Sound(name="Cruising Chauffeur is activated",
			filename="13.wav")
sound_cc_activated.tag_add(tag_information)
sound_cc_activated.tag_add(tag_female)
sound_dev_basic_brake = models.Sound(name="Basic brake",
			filename="14.wav")
sound_dev_basic_brake.tag_add(tag_signal)
sound_dev_basic_brake.tag_add(tag_fast)
sound_dev_basic_brake.tag_add(tag_urgent1)
sound_dev_basic_brake.tag_add(tag_stop)
sound_dev_basic_brake.tag_add(tag_steps)
sound_dev_basic_brake.tag_add(tag_dance)
sound_dev_basic_brake.tag_add(tag_jazz)
sound_dev_blink = models.Sound(name="Blink 3",
			filename="15.wav")
sound_dev_blink.tag_add(tag_accelerated)
sound_dev_blink.tag_add(tag_pushing)
sound_dev_blink.tag_add(tag_faster)
sound_dev_blink.tag_add(tag_something_happens)
sound_dev_blink.tag_add(tag_approach)
sound_dev_blink.tag_add(tag_pains)
sound_dev_vari2 = models.Sound(name="Vari2 EFX",
			filename="16.wav")
sound_dev_vari2.tag_add(tag_stone)
sound_dev_vari2.tag_add(tag_clapping)
sound_dev_vari2.tag_add(tag_click)
sound_dev_vari2.tag_add(tag_wooden)
sound_dev_vari2.tag_add(tag_strange)
sound_dev_vari2.tag_add(tag_instrument)
sound_dev_vari2.tag_add(tag_woodpecker)
sound_dev_vari2.tag_add(tag_winter)
sound_dev_vari2.tag_add(tag_nature)
sound_dev_vari2.tag_add(tag_water)
sound_dev_w7 = models.Sound(name="W7",
			filename="17.wav")
sound_dev_w7.tag_add(tag_higher_at_the_end)
sound_dev_w7.tag_add(tag_big_hall)
sound_dev_w7.tag_add(tag_steps)
sound_dev_w7.tag_add(tag_hurry)
sound_dev_w7.tag_add(tag_danger)
sound_dev_w7.tag_add(tag_persecution)
sound_dev_w7.tag_add(tag_underground)
sound_full_6sec= models.Sound(name="Full 6 dec",
			filename="18.wav")
sound_full_6sec.tag_add(tag_urgent1)
sound_full_6sec.tag_add(tag_high_pitch)
sound_full_6sec.tag_add(tag_crash)
sound_full_6sec.tag_add(tag_need_to_intervene)
sound_full_6sec.tag_add(tag_future)
sound_full_6sec.tag_add(tag_complex)
sound_full_6sec.tag_add(tag_automated)
sound_future_750ms = models.Sound(name="Future 750ms",
			filename="19.wav")
sound_future_750ms.tag_add(tag_beep)
sound_future_750ms.tag_add(tag_metallic)
sound_future_750ms.tag_add(tag_short)
sound_future_750ms.tag_add(tag_shutdown)
sound_future_750ms.tag_add(tag_electronic)
sound_future_750ms.tag_add(tag_synthetic)
sound_future_750ms.tag_add(tag_not_human)
sound_high_full = models.Sound(name="High full",
			filename="20.wav")
sound_high_full.tag_add(tag_knock)
sound_high_full.tag_add(tag_accelerated)
sound_high_full.tag_add(tag_traffic_lights)
sound_high_full.tag_add(tag_move)
sound_high_full.tag_add(tag_rhythm)
sound_nova_switch_off = models.Sound(name="Switch off",
			filename="21.wav")
sound_nova_switch_off.tag_add(tag_close)
sound_nova_switch_off.tag_add(tag_short)
sound_nova_switch_off.tag_add(tag_selection_in_menu)
sound_nova_switch_off.tag_add(tag_classic)
sound_nova_switch_off.tag_add(tag_accord)
sound_nova_switch_off.tag_add(tag_dull)
sound_nova_53 = models.Sound(name="Sound 5",
			filename="22.wav")
sound_nova_53.tag_add(tag_attention)
sound_nova_53.tag_add(tag_short)
sound_nova_53.tag_add(tag_metallic)
sound_nova_53.tag_add(tag_drawing)
sound_nova_53.tag_add(tag_demanding)
sound_nova_65 = models.Sound(name="Sound 6",
			filename="23.wav")
sound_nova_65.tag_add(tag_short)
sound_nova_65.tag_add(tag_strike)
sound_nova_65.tag_add(tag_move)
sound_nova_65.tag_add(tag_speed)
sound_nova_65.tag_add(tag_weather)
sound_nova_65.tag_add(tag_flash)
sound_uc1_activation_exc3 = models.Sound(name="Activation system error",
			filename="24.wav")
sound_uc1_activation_exc3.tag_add(tag_female)
sound_uc1_activation_exc3.tag_add(tag_information)
sound_uc1_activation_exc3.tag_add(tag_telephone)
sound_uc2_tor_notification = models.Sound(name="TOR notification",
			filename="25.wav")
sound_uc2_tor_notification.tag_add(tag_notification)
sound_uc2_tor_notification.tag_add(tag_information)
sound_uc2_tor_notification.tag_add(tag_short)
sound_uc2_tor_notification.tag_add(tag_shutdown_of_OS)
sound_uc2_tor_notification.tag_add(tag_jingle)
sound_uc2_tor_notification.tag_add(tag_wakeup)

sound_a13 = models.Sound(name="A_13",
			filename="26.mp3")
sound_a13.tag_add(tag_female)
sound_a13.tag_add(tag_sharp)
sound_a13.tag_add(tag_fast)
sound_a13.tag_add(tag_precise)
sound_a13.tag_add(tag_peaceful)
sound_a15 = models.Sound(name="A_15",
			filename="27.wav")
sound_a15.tag_add(tag_reverb)
sound_a15.tag_add(tag_volumnious)
sound_a15.tag_add(tag_urgent1)
sound_a15.tag_add(tag_nervous)
sound_a16= models.Sound(name="A_16",
			filename="28.wav")
sound_a16.tag_add(tag_short)
sound_a16.tag_add(tag_trash)
sound_a16.tag_add(tag_sport)
sound_a16.tag_add(tag_active)
sound_a16.tag_add(tag_movement)
sound_b12 = models.Sound(name="B_12",
			filename="29.mp3")
sound_b12.tag_add(tag_long)
sound_b12.tag_add(tag_slurred)
sound_b12.tag_add(tag_female)
sound_b12.tag_add(tag_peaceful)
sound_b13 = models.Sound(name="B_13",
			filename="30.wav")
sound_b13.tag_add(tag_nice)
sound_b13.tag_add(tag_positive)
sound_b13.tag_add(tag_acknowledge)
sound_b13.tag_add(tag_computer)
sound_b13.tag_add(tag_opening)
sound_b17 = models.Sound(name="B_17",
			filename="31.wav")
sound_b17.tag_add(tag_short)
sound_b17.tag_add(tag_positive)
sound_b19 = models.Sound(name="B_19",
			filename="32.wav")
sound_b19.tag_add(tag_wave)
sound_b19.tag_add(tag_negative)
sound_b19.tag_add(tag_notification)
sound_b19.tag_add(tag_sudden)
sound_dev_brake = models.Sound(name="Brake dev",
			filename="33.wav")
sound_b12.tag_add(tag_playful)
sound_b12.tag_add(tag_fussy)
sound_b12.tag_add(tag_starting)
sound_b12.tag_add(tag_transition)
sound_discontinue_steering = models.Sound(name="Discontinue steering and pedal use",
			filename="34.wav")
sound_discontinue_steering.tag_add(tag_informative)
sound_discontinue_steering.tag_add(tag_long)
sound_discontinue_steering.tag_add(tag_precise)
sound_discontinue_steering.tag_add(tag_female)
sound_discontinue_steering.tag_add(tag_sad)
sound_detected_error = models.Sound(name="Due to detected error",
			filename="35.wav")
sound_detected_error.tag_add(tag_unprecise)
sound_detected_error.tag_add(tag_female)
sound_detected_error.tag_add(tag_sad)
sound_excessive_speed = models.Sound(name="Due to excessive speed",
			filename="36.wav")
sound_excessive_speed.tag_add(tag_precise)
sound_excessive_speed.tag_add(tag_informative)
sound_excessive_speed.tag_add(tag_clear)
sound_excessive_speed.tag_add(tag_female)
sound_excessive_speed.tag_add(tag_sad)
sound_default_overlay = models.Sound(name="Default overlay full",
			filename="37.wav")
sound_default_overlay.tag_add(tag_warning)
sound_default_overlay.tag_add(tag_metallic)
sound_default_overlay.tag_add(tag_unusual)
sound_subtle_750 = models.Sound(name="Subtle overlay full",
			filename="38.wav")
sound_subtle_750.tag_add(tag_high)
sound_subtle_750.tag_add(tag_fast)
sound_subtle_750.tag_add(tag_warning)
sound_subtle_750.tag_add(tag_metallic)
sound_nova_switch_on = models.Sound(name="Switch on",
			filename="39.wav")
sound_nova_switch_on.tag_add(tag_reverb)
sound_nova_switch_on.tag_add(tag_short)
sound_nova_switch_on.tag_add(tag_on)
sound_nove_manoevre = models.Sound(name="Manoevre",
			filename="40.aiff")
sound_nove_manoevre.tag_add(tag_metallic)
sound_nove_manoevre.tag_add(tag_short)
sound_nove_manoevre.tag_add(tag_fast)
sound_nove_manoevre.tag_add(tag_on)
sound_nova_safety_assist = models.Sound(name="Safety assist",
			filename="41.mp3")
sound_nova_safety_assist.tag_add(tag_short)
sound_nova_safety_assist.tag_add(tag_fast)
sound_nova_safety_assist.tag_add(tag_on)
sound_nova_indicator = models.Sound(name="Indicator",
			filename="42.mp3")
sound_nova_indicator.tag_add(tag_reverb)
sound_nova_indicator.tag_add(tag_popup)
sound_nova_indicator.tag_add(tag_short)
sound_nova_indicator.tag_add(tag_fast)
sound_nova_indicator.tag_add(tag_on)
sound_nova_10 = models.Sound(name="Sound 10",
			filename="43.ogg")
sound_nova_10.tag_add(tag_sharp)
sound_nova_10.tag_add(tag_short)
sound_nova_10.tag_add(tag_fast)
sound_nova_10.tag_add(tag_notification)
sound_nova_10.tag_add(tag_transition)
sound_nova_9 = models.Sound(name="Sound 9",
			filename="44.ogg")
sound_nova_9.tag_add(tag_shorter)
sound_nova_9.tag_add(tag_hard_to_hear)
sound_uc1_activation = models.Sound(name="Assistant activated",
			filename="45.wav")
sound_uc1_activation.tag_add(tag_reverb)
sound_uc1_activation.tag_add(tag_positive)
sound_uc1_activation.tag_add(tag_informative)
sound_uc1_activation.tag_add(tag_nice)
sound_uc1_activation.tag_add(tag_female)
sound_uc1_activation.tag_add(tag_happy)
sound_uc2_tor = models.Sound(name="TOR speeding",
			filename="46.ogg")
sound_uc2_tor.tag_add(tag_long)
sound_uc2_tor.tag_add(tag_informative)
sound_uc2_tor.tag_add(tag_positive)
sound_uc2_tor.tag_add(tag_female)
sound_uc2_tor.tag_add(tag_sad)
sound_uc2_system_error = models.Sound(name="TOR system error",
			filename="47.wav")
sound_uc2_system_error.tag_add(tag_short)
sound_uc2_system_error.tag_add(tag_warning)
sound_uc2_system_error.tag_add(tag_positive)
sound_uc2_system_error.tag_add(tag_misleading)
sound_uc2_system_error.tag_add(tag_female)
sound_uc2_system_error.tag_add(tag_angry)
sound_urgent_takeover = models.Sound(name="Urgent TOR",
			filename="48.ogg")
sound_urgent_takeover.tag_add(tag_warning)
sound_urgent_takeover.tag_add(tag_negative)
sound_urgent_takeover.tag_add(tag_sharp)
sound_urgent_takeover.tag_add(tag_precise)
sound_urgent_takeover.tag_add(tag_urgent1)
sound_urgent_takeover.tag_add(tag_tor)
sound_urgent_takeover.tag_add(tag_fast)
sound_user_error = models.Sound(name="User error",
			filename="49.wav")
sound_user_error.tag_add(tag_wrong)
sound_user_error.tag_add(tag_reverb)
sound_user_error.tag_add(tag_neutral)
sound_user_error.tag_add(tag_warning)
sound_user_error_important = models.Sound(name="User error important",
			filename="50.wav")
sound_user_error_important.tag_add(tag_wrong)
sound_user_error_important.tag_add(tag_reverb)
sound_user_error_important.tag_add(tag_negative)
sound_user_error_important.tag_add(tag_warning)

db.session.add(sound_a1)
db.session.add(sound_a11)
db.session.add(sound_a18)
db.session.add(sound_a23)
db.session.add(sound_a7)
db.session.add(sound_a8)
db.session.add(sound_ad_deactivation)
db.session.add(sound_ad_notification)
db.session.add(sound_b23)
db.session.add(sound_b25)
db.session.add(sound_b3)
db.session.add(sound_b7)
db.session.add(sound_cc_activated)
db.session.add(sound_dev_basic_brake)
db.session.add(sound_dev_blink)
db.session.add(sound_dev_vari2)
db.session.add(sound_dev_w7)
db.session.add(sound_full_6sec)
db.session.add(sound_future_750ms)
db.session.add(sound_high_full)
db.session.add(sound_nova_switch_off)
db.session.add(sound_nova_53)
db.session.add(sound_nova_65)
db.session.add(sound_uc1_activation_exc3)
db.session.add(sound_uc2_tor_notification)

db.session.add(sound_a13)
db.session.add(sound_a15)
db.session.add(sound_a16)
db.session.add(sound_b12)
db.session.add(sound_b13)
db.session.add(sound_b17)
db.session.add(sound_b19)
db.session.add(sound_dev_brake)
db.session.add(sound_discontinue_steering)
db.session.add(sound_detected_error)
db.session.add(sound_excessive_speed)
db.session.add(sound_default_overlay)
db.session.add(sound_subtle_750)
db.session.add(sound_nova_switch_on)
db.session.add(sound_nove_manoevre)
db.session.add(sound_nova_safety_assist)
db.session.add(sound_nova_indicator)
db.session.add(sound_nova_10)
db.session.add(sound_nova_9)
db.session.add(sound_uc1_activation)
db.session.add(sound_uc2_tor)
db.session.add(sound_uc2_system_error)
db.session.add(sound_urgent_takeover)
db.session.add(sound_user_error)
db.session.add(sound_user_error_important)

views.update_tags_json()
views.update_sounds_json()
db.session.commit()

################## Tester 1 ##################
# Add users
test_user = models.ClientUser(nickname="stephan_cieler",
				first_name="Stephan",
				last_name="Cieler",
                email="stephan.cieler@continental-corporation.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
jim = models.ClientUser(nickname="jim_clark",
				first_name="Jim",
				last_name="Clark",
                email="wordsforsound.jim@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
ayrton = models.SupplierUser(nickname="ayrton_senna",
				first_name="Ayrton",
				last_name="Senna",
                email="wordsforsound.ayrton@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
michael = models.SupplierUser(nickname="michael_schumacher",
				first_name="Michael",
				last_name="Schumacher",
                email="wordsforsound.michael@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
niki = models.SupplierUser(nickname="niki_lauda",
				first_name="Niki",
				last_name="Lauda",
                email="wordsforsound.niki@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=False)
db.session.add(test_user)
db.session.add(jim)
db.session.add(ayrton)
db.session.add(michael)
db.session.add(niki)
db.session.commit()

# Add projects
project_auditory_test = models.Project(name="AD overtaking",
				description="In this we will be developing auditory assets for take-over requests during highly automated driving.",
				filename="icad 2015.pdf",
				finished=False,
				user=test_user,
				timestamp=datetime.now())
db.session.add(project_auditory_test)
db.session.commit()

# Add assets
asset1 = models.Asset(name="Beep for left overtaking",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		status=models.AssetStatus.iteration.value,
        		project=project_auditory_test,
        		finished=False,
        		iteration_number=0,
        		timestamp=datetime.now(),
        		notify_by_email=True)
asset2 = models.Asset(name="Beep for right overtaking",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                status=models.AssetStatus.iteration.value,
                project=project_auditory_test,
                finished=False,
                iteration_number=0,
                timestamp=datetime.now(),
                notify_by_email=True)
description1 = models.Description(duration="200",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		sound_type=1,
                sound_family=1,
        		pitch="B#",
        		user=test_user,
        		timestamp=datetime.now())
description1.tag_add(tag_beep)
description1.tag_add(tag_urgent4)
description1.tag_add(tag_warning)
description1.tag_add(tag_positive)
description1.tag_add(tag_metallic)
description1.sound_add(sound_beep_freezman)
description1.sound_add(sound_uc2_system_error)
description1.sound_add(sound_b19)
description2 = models.Description(duration="65",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                sound_type=1,
                sound_family=1,
                pitch="A",
                user=test_user,
                timestamp=datetime.now())
description2.tag_add(tag_beep)
description2.tag_add(tag_urgent2)
description2.tag_add(tag_warning)
description2.tag_add(tag_negative)
description2.tag_add(tag_wooden)
description2.tag_add(tag_worthy)
description2.sound_add(sound_beep_freezman)
description2.sound_add(sound_b13)
description2.sound_add(sound_a16)
description2.sound_add(sound_b17)
db.session.add(asset1)
db.session.add(asset2)

asset1.description_add(description1)
asset2.description_add(description2)

asset1.client_add(test_user)
asset1.client_add(jim)
asset1.supplier_add(michael)
asset1.supplier_add(niki)

asset2.client_add(test_user)
asset2.supplier_add(ayrton)

asset1.init_in_hands()
asset2.init_in_hands()

project_auditory_test.asset_add(asset1)
project_auditory_test.asset_add(asset2)
db.session.commit()


################## Tester 2 ##################
# Add users
test_user = models.ClientUser(nickname="daria_nikulina",
				first_name="Daria",
				last_name="Nikulina",
                email="daria.k.nikulina@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
jim = models.ClientUser(nickname="jim_clark2",
				first_name="Jim",
				last_name="Clark",
                email="wordsforsound.jim2@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="jim_70.jpg")
ayrton = models.SupplierUser(nickname="ayrton_senna2",
				first_name="Ayrton",
				last_name="Senna",
                email="wordsforsound.ayrton2@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="ayrton_70.jpg")
michael = models.SupplierUser(nickname="michael_schumacher2",
				first_name="Michael",
				last_name="Schumacher",
                email="wordsforsound.michael2@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="michael_70.jpg")
niki = models.SupplierUser(nickname="niki_lauda2",
				first_name="Niki",
				last_name="Lauda",
                email="wordsforsound.niki2@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=False,
                avatar_filename="niki_70.jpg")
db.session.add(test_user)
db.session.add(jim)
db.session.add(ayrton)
db.session.add(michael)
db.session.add(niki)
db.session.commit()

# Add projects
project_auditory_test = models.Project(name="AD overtaking 2",
				description="In this we will be developing auditory assets for take-over requests during highly automated driving.",
				filename="icad 2015.pdf",
				finished=False,
				user=test_user,
				timestamp=datetime.now())
db.session.add(project_auditory_test)
db.session.commit()

# Add assets
asset1 = models.Asset(name="Beep for left overtaking",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		status=models.AssetStatus.iteration.value,
        		project=project_auditory_test,
        		finished=False,
        		iteration_number=0,
        		timestamp=datetime.now(),
        		notify_by_email=True)
asset2 = models.Asset(name="Beep for right overtaking",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                status=models.AssetStatus.iteration.value,
                project=project_auditory_test,
                finished=False,
                iteration_number=0,
                timestamp=datetime.now(),
                notify_by_email=True)
description1 = models.Description(duration="200",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		sound_type=1,
                sound_family=1,
        		pitch="B#",
        		user=test_user,
        		timestamp=datetime.now())
description1.tag_add(tag_beep)
description1.tag_add(tag_urgent4)
description1.tag_add(tag_warning)
description1.tag_add(tag_positive)
description1.tag_add(tag_metallic)
description1.sound_add(sound_beep_freezman)
description1.sound_add(sound_uc2_system_error)
description1.sound_add(sound_b19)
description2 = models.Description(duration="65",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                sound_type=1,
                sound_family=1,
                pitch="A",
                user=test_user,
                timestamp=datetime.now())
description2.tag_add(tag_beep)
description2.tag_add(tag_urgent2)
description2.tag_add(tag_warning)
description2.tag_add(tag_negative)
description2.tag_add(tag_wooden)
description2.tag_add(tag_worthy)
description2.sound_add(sound_beep_freezman)
description2.sound_add(sound_b13)
description2.sound_add(sound_a16)
description2.sound_add(sound_b17)
db.session.add(asset1)
db.session.add(asset2)

asset1.description_add(description1)
asset2.description_add(description2)

asset1.client_add(test_user)
asset1.client_add(jim)
asset1.supplier_add(michael)
asset1.supplier_add(niki)

asset2.client_add(test_user)
asset2.supplier_add(ayrton)

asset1.init_in_hands()
asset2.init_in_hands()

project_auditory_test.asset_add(asset1)
project_auditory_test.asset_add(asset2)
db.session.commit()

################## Tester 3 ##################
# Add users
test_user = models.ClientUser(nickname="benjamin_mathe",
				first_name="Benjamin",
				last_name="Mathe",
                email="benjamin.mathe@continental-corporation.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
jim = models.ClientUser(nickname="jim_clark3",
				first_name="Jim",
				last_name="Clark",
                email="wordsforsound.jim3@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="jim_70.jpg")
ayrton = models.SupplierUser(nickname="ayrton_senna3",
				first_name="Ayrton",
				last_name="Senna",
                email="wordsforsound.ayrton3@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="ayrton_70.jpg")
michael = models.SupplierUser(nickname="michael_schumacher3",
				first_name="Michael",
				last_name="Schumacher",
                email="wordsforsound.michael3@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="michael_70.jpg")
niki = models.SupplierUser(nickname="niki_lauda3",
				first_name="Niki",
				last_name="Lauda",
                email="wordsforsound.niki3@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=False,
                avatar_filename="niki_70.jpg")
db.session.add(test_user)
db.session.add(jim)
db.session.add(ayrton)
db.session.add(michael)
db.session.add(niki)
db.session.commit()

# Add projects
project_auditory_test = models.Project(name="AD overtaking 3",
				description="In this we will be developing auditory assets for take-over requests during highly automated driving.",
				filename="icad 2015.pdf",
				finished=False,
				user=test_user,
				timestamp=datetime.now())
db.session.add(project_auditory_test)
db.session.commit()

# Add assets
asset1 = models.Asset(name="Beep for left overtaking",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		status=models.AssetStatus.iteration.value,
        		project=project_auditory_test,
        		finished=False,
        		iteration_number=0,
        		timestamp=datetime.now(),
        		notify_by_email=True)
asset2 = models.Asset(name="Beep for right overtaking",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                status=models.AssetStatus.iteration.value,
                project=project_auditory_test,
                finished=False,
                iteration_number=0,
                timestamp=datetime.now(),
                notify_by_email=True)
description1 = models.Description(duration="200",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		sound_type=1,
                sound_family=1,
        		pitch="B#",
        		user=test_user,
        		timestamp=datetime.now())
description1.tag_add(tag_beep)
description1.tag_add(tag_urgent4)
description1.tag_add(tag_warning)
description1.tag_add(tag_positive)
description1.tag_add(tag_metallic)
description1.sound_add(sound_beep_freezman)
description1.sound_add(sound_uc2_system_error)
description1.sound_add(sound_b19)
description2 = models.Description(duration="65",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                sound_type=1,
                sound_family=1,
                pitch="A",
                user=test_user,
                timestamp=datetime.now())
description2.tag_add(tag_beep)
description2.tag_add(tag_urgent2)
description2.tag_add(tag_warning)
description2.tag_add(tag_negative)
description2.tag_add(tag_wooden)
description2.tag_add(tag_worthy)
description2.sound_add(sound_beep_freezman)
description2.sound_add(sound_b13)
description2.sound_add(sound_a16)
description2.sound_add(sound_b17)
db.session.add(asset1)
db.session.add(asset2)

asset1.description_add(description1)
asset2.description_add(description2)

asset1.client_add(test_user)
asset1.client_add(jim)
asset1.supplier_add(michael)
asset1.supplier_add(niki)

asset2.client_add(test_user)
asset2.supplier_add(ayrton)

asset1.init_in_hands()
asset2.init_in_hands()

project_auditory_test.asset_add(asset1)
project_auditory_test.asset_add(asset2)
db.session.commit()

################## Tester 4 ##################
# Add users
test_user = models.ClientUser(nickname="joerg_witthaus",
				first_name="Joerg",
				last_name="Witthaus",
                email="joerg.witthaus@continental-corporation.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
jim = models.ClientUser(nickname="jim_clark4",
				first_name="Jim",
				last_name="Clark",
                email="wordsforsound.jim4@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="jim_70.jpg")
ayrton = models.SupplierUser(nickname="ayrton_senna4",
				first_name="Ayrton",
				last_name="Senna",
                email="wordsforsound.ayrton4@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="ayrton_70.jpg")
michael = models.SupplierUser(nickname="michael_schumacher4",
				first_name="Michael",
				last_name="Schumacher",
                email="wordsforsound.michael4@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="michael_70.jpg")
niki = models.SupplierUser(nickname="niki_lauda4",
				first_name="Niki",
				last_name="Lauda",
                email="wordsforsound.niki4@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=False,
                avatar_filename="niki_70.jpg")
db.session.add(test_user)
db.session.add(jim)
db.session.add(ayrton)
db.session.add(michael)
db.session.add(niki)
db.session.commit()

# Add projects
project_auditory_test = models.Project(name="AD overtaking 4",
				description="In this we will be developing auditory assets for take-over requests during highly automated driving.",
				filename="icad 2015.pdf",
				finished=False,
				user=test_user,
				timestamp=datetime.now())
db.session.add(project_auditory_test)
db.session.commit()

# Add assets
asset1 = models.Asset(name="Beep for left overtaking",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		status=models.AssetStatus.iteration.value,
        		project=project_auditory_test,
        		finished=False,
        		iteration_number=0,
        		timestamp=datetime.now(),
        		notify_by_email=True)
asset2 = models.Asset(name="Beep for right overtaking",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                status=models.AssetStatus.iteration.value,
                project=project_auditory_test,
                finished=False,
                iteration_number=0,
                timestamp=datetime.now(),
                notify_by_email=True)
description1 = models.Description(duration="200",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		sound_type=1,
                sound_family=1,
        		pitch="B#",
        		user=test_user,
        		timestamp=datetime.now())
description1.tag_add(tag_beep)
description1.tag_add(tag_urgent4)
description1.tag_add(tag_warning)
description1.tag_add(tag_positive)
description1.tag_add(tag_metallic)
description1.sound_add(sound_beep_freezman)
description1.sound_add(sound_uc2_system_error)
description1.sound_add(sound_b19)
description2 = models.Description(duration="65",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                sound_type=1,
                sound_family=1,
                pitch="A",
                user=test_user,
                timestamp=datetime.now())
description2.tag_add(tag_beep)
description2.tag_add(tag_urgent2)
description2.tag_add(tag_warning)
description2.tag_add(tag_negative)
description2.tag_add(tag_wooden)
description2.tag_add(tag_worthy)
description2.sound_add(sound_beep_freezman)
description2.sound_add(sound_b13)
description2.sound_add(sound_a16)
description2.sound_add(sound_b17)
db.session.add(asset1)
db.session.add(asset2)

asset1.description_add(description1)
asset2.description_add(description2)

asset1.client_add(test_user)
asset1.client_add(jim)
asset1.supplier_add(michael)
asset1.supplier_add(niki)

asset2.client_add(test_user)
asset2.supplier_add(ayrton)

asset1.init_in_hands()
asset2.init_in_hands()

project_auditory_test.asset_add(asset1)
project_auditory_test.asset_add(asset2)
db.session.commit()

################## Tester 5 ##################
# Add users
test_user = models.ClientUser(nickname="roman_pogribnyi",
				first_name="Roman",
				last_name="Pogribnyi",
                email="pogribnyi@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
jim = models.ClientUser(nickname="jim_clark5",
				first_name="Jim",
				last_name="Clark",
                email="wordsforsound.jim5@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="jim_70.jpg")
ayrton = models.SupplierUser(nickname="ayrton_senna5",
				first_name="Ayrton",
				last_name="Senna",
                email="wordsforsound.ayrton5@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="ayrton_70.jpg")
michael = models.SupplierUser(nickname="michael_schumacher5",
				first_name="Michael",
				last_name="Schumacher",
                email="wordsforsound.michael5@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="michael_70.jpg")
niki = models.SupplierUser(nickname="niki_lauda5",
				first_name="Niki",
				last_name="Lauda",
                email="wordsforsound.niki5@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=False,
                avatar_filename="niki_70.jpg")
db.session.add(test_user)
db.session.add(jim)
db.session.add(ayrton)
db.session.add(michael)
db.session.add(niki)
db.session.commit()

# Add projects
project_auditory_test = models.Project(name="AD overtaking 3",
				description="In this we will be developing auditory assets for take-over requests during highly automated driving.",
				filename="icad 2015.pdf",
				finished=False,
				user=test_user,
				timestamp=datetime.now())
db.session.add(project_auditory_test)
db.session.commit()

# Add assets
asset1 = models.Asset(name="Beep for left overtaking",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		status=models.AssetStatus.iteration.value,
        		project=project_auditory_test,
        		finished=False,
        		iteration_number=0,
        		timestamp=datetime.now(),
        		notify_by_email=True)
asset2 = models.Asset(name="Beep for right overtaking",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                status=models.AssetStatus.iteration.value,
                project=project_auditory_test,
                finished=False,
                iteration_number=0,
                timestamp=datetime.now(),
                notify_by_email=True)
description1 = models.Description(duration="200",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		sound_type=1,
                sound_family=1,
        		pitch="B#",
        		user=test_user,
        		timestamp=datetime.now())
description1.tag_add(tag_beep)
description1.tag_add(tag_urgent4)
description1.tag_add(tag_warning)
description1.tag_add(tag_positive)
description1.tag_add(tag_metallic)
description1.sound_add(sound_beep_freezman)
description1.sound_add(sound_uc2_system_error)
description1.sound_add(sound_b19)
description2 = models.Description(duration="65",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                sound_type=1,
                sound_family=1,
                pitch="A",
                user=test_user,
                timestamp=datetime.now())
description2.tag_add(tag_beep)
description2.tag_add(tag_urgent2)
description2.tag_add(tag_warning)
description2.tag_add(tag_negative)
description2.tag_add(tag_wooden)
description2.tag_add(tag_worthy)
description2.sound_add(sound_beep_freezman)
description2.sound_add(sound_b13)
description2.sound_add(sound_a16)
description2.sound_add(sound_b17)
db.session.add(asset1)
db.session.add(asset2)

asset1.description_add(description1)
asset2.description_add(description2)

asset1.client_add(test_user)
asset1.client_add(jim)
asset1.supplier_add(michael)
asset1.supplier_add(niki)

asset2.client_add(test_user)
asset2.supplier_add(ayrton)

asset1.init_in_hands()
asset2.init_in_hands()

project_auditory_test.asset_add(asset1)
project_auditory_test.asset_add(asset2)
db.session.commit()

################## Tester 6 ##################
# Add users
test_user = models.ClientUser(nickname="joost_de_winter",
				first_name="Joost",
				last_name="De Winter",
                email="jcfdewinter@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
jim = models.ClientUser(nickname="jim_clark6",
				first_name="Jim",
				last_name="Clark",
                email="wordsforsound.jim6@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="jim_70.jpg")
ayrton = models.SupplierUser(nickname="ayrton_senna6",
				first_name="Ayrton",
				last_name="Senna",
                email="wordsforsound.ayrton6@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="ayrton_70.jpg")
michael = models.SupplierUser(nickname="michael_schumacher6",
				first_name="Michael",
				last_name="Schumacher",
                email="wordsforsound.michael6@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True,
                avatar_filename="michael_70.jpg")
niki = models.SupplierUser(nickname="niki_lauda6",
				first_name="Niki",
				last_name="Lauda",
                email="wordsforsound.niki6@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=False,
                avatar_filename="niki_70.jpg")
db.session.add(test_user)
db.session.add(jim)
db.session.add(ayrton)
db.session.add(michael)
db.session.add(niki)
db.session.commit()

# Add projects
project_auditory_test = models.Project(name="AD overtaking 5",
				description="In this we will be developing auditory assets for take-over requests during highly automated driving.",
				filename="icad 2015.pdf",
				finished=False,
				user=test_user,
				timestamp=datetime.now())
db.session.add(project_auditory_test)
db.session.commit()

# Add assets
asset1 = models.Asset(name="Beep for left overtaking",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		status=models.AssetStatus.iteration.value,
        		project=project_auditory_test,
        		finished=False,
        		iteration_number=0,
        		timestamp=datetime.now(),
        		notify_by_email=True)
asset2 = models.Asset(name="Beep for right overtaking",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                status=models.AssetStatus.iteration.value,
                project=project_auditory_test,
                finished=False,
                iteration_number=0,
                timestamp=datetime.now(),
                notify_by_email=True)
description1 = models.Description(duration="200",
				description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than 3 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, happy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). Input: speed of automated car, TTC, safest maneuver trajectory.",
        		sound_type=1,
                sound_family=1,
        		pitch="B#",
        		user=test_user,
        		timestamp=datetime.now())
description1.tag_add(tag_beep)
description1.tag_add(tag_urgent4)
description1.tag_add(tag_warning)
description1.tag_add(tag_positive)
description1.tag_add(tag_metallic)
description1.sound_add(sound_beep_freezman)
description1.sound_add(sound_uc2_system_error)
description1.sound_add(sound_b19)
description2 = models.Description(duration="65",
				description="Non-urgent take-over request (TTC less than 10 sec) with information on an object in the blind-spot in the left lane, behind the automated car (driving on the middle lane). It should sound non-intrusive, worthy, modern and electric, similar to sounds employed by Volvo in their newest cars. Input: speed of automated car, TTC, location of object in blind spot relative to automated car. Could involve speech by a female actor with US English accent.",
                sound_type=1,
                sound_family=1,
                pitch="A",
                user=test_user,
                timestamp=datetime.now())
description2.tag_add(tag_beep)
description2.tag_add(tag_urgent2)
description2.tag_add(tag_warning)
description2.tag_add(tag_negative)
description2.tag_add(tag_wooden)
description2.tag_add(tag_worthy)
description2.sound_add(sound_beep_freezman)
description2.sound_add(sound_b13)
description2.sound_add(sound_a16)
description2.sound_add(sound_b17)
db.session.add(asset1)
db.session.add(asset2)

asset1.description_add(description1)
asset2.description_add(description2)

asset1.client_add(test_user)
asset1.client_add(jim)
asset1.supplier_add(michael)
asset1.supplier_add(niki)

asset2.client_add(test_user)
asset2.supplier_add(ayrton)

asset1.init_in_hands()
asset2.init_in_hands()

project_auditory_test.asset_add(asset1)
project_auditory_test.asset_add(asset2)
db.session.commit()