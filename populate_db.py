from app import db, models, views
from datetime import datetime

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
tag_tor = models.Tag(name="TOR")
tag_sharp = models.Tag(name="sharp")
tag_tor = models.Tag(name="TOR")
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

# Add custom sounds
sound_beep_freezman = models.Sound(name="Beep freezman",
			filename="153213__freezeman__beep1.wav",
			rights="CC Attribution License")
sound_beep_freezman.tag_add(tag_beep)
sound_beep_freezman.tag_add(tag_urgent2)
sound_beep_freezman.tag_add(tag_long)
sound_beep_freezman.tag_add(tag_worthy)

db.session.add(sound_beep_freezman)

db.session.commit()

# Add sounds from projects
sound_a13 = models.Sound(name="A_13.wav",
			filename="A_13.wav")
sound_a13.tag_add(tag_female)
sound_a13.tag_add(tag_sharp)
sound_a13.tag_add(tag_fast)
sound_a13.tag_add(tag_precise)
sound_a13.tag_add(tag_peaceful)
sound_a15 = models.Sound(name="A_15.wav",
			filename="A_15.wav")
sound_a15.tag_add(tag_reverb)
sound_a15.tag_add(tag_volumnious)
sound_a15.tag_add(tag_urgent)
sound_a15.tag_add(tag_nervous)
sound_a16= models.Sound(name="A_16.wav",
			filename="A_16.wav")
sound_a16.tag_add(tag_short)
sound_a16.tag_add(tag_trash)
sound_a16.tag_add(tag_sport)
sound_a16.tag_add(tag_active)
sound_a16.tag_add(tag_movement)
sound_b12 = models.Sound(name="B_12.wav",
			filename="B_12.wav")
sound_b12.tag_add(tag_long)
sound_b12.tag_add(tag_slurred)
sound_b12.tag_add(tag_female)
sound_b12.tag_add(tag_peaceful)
sound_b13 = models.Sound(name="B_13.wav",
			filename="B_13.wav")
sound_b13.tag_add(tag_nice)
sound_b13.tag_add(tag_positive)
sound_b13.tag_add(tag_acknowledge)
sound_b13.tag_add(tag_computer)
sound_b13.tag_add(tag_opening)
sound_b17 = models.Sound(name="B_17.wav",
			filename="B_17.wav")
sound_b17.tag_add(tag_short)
sound_b17.tag_add(tag_positive)
sound_b19 = models.Sound(name="B_19.wav",
			filename="B_19.wav")
sound_b19.tag_add(tag_wave)
sound_b19.tag_add(tag_negative)
sound_b19.tag_add(tag_notification)
sound_b19.tag_add(tag_sudden)
sound_dev_brake = models.Sound(name="Brake dev",
			filename="DEV_BRAKE.wav")
sound_b12.tag_add(tag_playful)
sound_b12.tag_add(tag_fussy)
sound_b12.tag_add(tag_starting)
sound_b12.tag_add(tag_transition)
sound_discontinue_steering = models.Sound(name="Discontinue steering and Ppdal use",
			filename="Discontinue Steering and Pedal Use.wav")
sound_discontinue_steering.tag_add(tag_informative)
sound_discontinue_steering.tag_add(tag_long)
sound_discontinue_steering.tag_add(tag_precise)
sound_discontinue_steering.tag_add(tag_female)
sound_discontinue_steering.tag_add(tag_sad)
sound_detected_error = models.Sound(name="Due to detected error",
			filename="due to detected error.wav")
sound_detected_error.tag_add(tag_unprecise)
sound_detected_error.tag_add(tag_female)
sound_detected_error.tag_add(tag_sad)
sound_excessive_speed = models.Sound(name="Due to excessive speed",
			filename="Due to excessive speed.wav")
sound_excessive_speed.tag_add(tag_precise)
sound_excessive_speed.tag_add(tag_informative)
sound_excessive_speed.tag_add(tag_clear)
sound_excessive_speed.tag_add(tag_female)
sound_excessive_speed.tag_add(tag_sad)
sound_default_overlay = models.Sound(name="Default overlay full",
			filename="FINAL_Default_Overlay_Full_750.wav")
sound_default_overlay.tag_add(tag_warning)
sound_default_overlay.tag_add(tag_metallic)
sound_default_overlay.tag_add(tag_unusual)
sound_subtle_750 = models.Sound(name="Subtle overlay full",
			filename="FINAL_Subtle_750_OverlayFull.wav")
sound_subtle_750.tag_add(tag_high)
sound_subtle_750.tag_add(tag_fast)
sound_subtle_750.tag_add(tag_warning)
sound_subtle_750.tag_add(tag_metallic)
sound_nova_switch_on = models.Sound(name="Switch on (Nova)",
			filename="Project_Nova_01_SwitchOn.wav")
sound_nova_switch_on.tag_add(tag_reverb)
sound_nova_switch_on.tag_add(tag_short)
sound_nova_switch_on.tag_add(tag_on)
sound_nove_manoevre = models.Sound(name="Manoevre (Nova)",
			filename="Project_Nova_03_Manoevre.wav")
sound_nove_manoevre.tag_add(tag_metallic)
sound_nove_manoevre.tag_add(tag_short)
sound_nove_manoevre.tag_add(tag_fast)
sound_nove_manoevre.tag_add(tag_on)
sound_nova_safety_assist = models.Sound(name="Safety assist (Nova)",
			filename="Project_Nova_06_SafetyAssist_Lv1.wav")
sound_nova_safety_assist.tag_add(tag_short)
sound_nova_safety_assist.tag_add(tag_fast)
sound_nova_safety_assist.tag_add(tag_on)
sound_nova_indicator = models.Sound(name="Indicator (Nova)",
			filename="Project_Nova_09_Indicator.wav")
sound_nova_indicator.tag_add(tag_reverb)
sound_nova_indicator.tag_add(tag_popup)
sound_nova_indicator.tag_add(tag_short)
sound_nova_indicator.tag_add(tag_fast)
sound_nova_indicator.tag_add(tag_on)
sound_nova_10 = models.Sound(name="Sound 10 (Nova)",
			filename="Project_Nova_10_2_v2.wav")
sound_nova_10.tag_add(tag_sharp)
sound_nova_10.tag_add(tag_short)
sound_nova_10.tag_add(tag_fast)
sound_nova_10.tag_add(tag_notification)
sound_nova_10.tag_add(tag_transition)
sound_nova_9 = models.Sound(name="Sound 9 (Nova)",
			filename="Project_Nova_9_4_On.wav")
sound_nova_9.tag_add(tag_shorter)
sound_nova_9.tag_add(tag_hard_to_hear)
sound_uc1_activation = models.Sound(name="CC activated",
			filename="UC1_Activation_CC_Activated.wav")
sound_uc1_activation.tag_add(tag_reverb)
sound_uc1_activation.tag_add(tag_positive)
sound_uc1_activation.tag_add(tag_informative)
sound_uc1_activation.tag_add(tag_nice)
sound_uc1_activation.tag_add(tag_female)
sound_uc1_activation.tag_add(tag_happy)
sound_uc2_tor = models.Sound(name="TOR speeding",
			filename="UC2_TOR_speeding.wav")
sound_uc2_tor.tag_add(tag_long)
sound_uc2_tor.tag_add(tag_informative)
sound_uc2_tor.tag_add(tag_positive)
sound_uc2_tor.tag_add(tag_female)
sound_uc2_tor.tag_add(tag_sad)
sound_uc2_system_error = models.Sound(name="TOR system error",
			filename="UC2_TOR_system_error.wav")
sound_uc2_system_error.tag_add(tag_short)
sound_uc2_system_error.tag_add(tag_warning)
sound_uc2_system_error.tag_add(tag_positive)
sound_uc2_system_error.tag_add(tag_misleading)
sound_uc2_system_error.tag_add(tag_female)
sound_uc2_system_error.tag_add(tag_angry)
sound_urgent_takeover = models.Sound(name="Urgent TOR",
			filename="URGENT_TAKEOVER.wav")
sound_urgent_takeover.tag_add(tag_warning)
sound_urgent_takeover.tag_add(tag_negative)
sound_urgent_takeover.tag_add(tag_sharp)
sound_urgent_takeover.tag_add(tag_precise)
sound_urgent_takeover.tag_add(tag_urgent1)
sound_urgent_takeover.tag_add(tag_tor)
sound_urgent_takeover.tag_add(tag_fast)
sound_user_error = models.Sound(name="User error",
			filename="User_Error.wav")
sound_user_error.tag_add(tag_wrong)
sound_user_error.tag_add(tag_reverb)
sound_user_error.tag_add(tag_neutral)
sound_user_error.tag_add(tag_warning)
sound_user_error_important = models.Sound(name="User error important",
			filename="User_Error_Important.wav")
sound_user_error_important.tag_add(tag_wrong)
sound_user_error_important.tag_add(tag_reverb)
sound_user_error_important.tag_add(tag_negative)
sound_user_error_important.tag_add(tag_warning)

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

# Add users
pb = models.ClientUser(nickname="Pavlo Bazilinskyy",
				first_name="Pavlo",
				last_name="Bazilinskyy",
                email="pavlo.bazilinskyy@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
dm = models.ClientUser(nickname="Diego Montoya",
				first_name="Stephan",
				last_name="Cieler",
                email="Diego.Montoya@gmail1.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
ase = models.SupplierUser(nickname="Ayrton Senna",
				first_name="Ayrton",
				last_name="Senna",
                email="hollgam@gmail.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
ms = models.SupplierUser(nickname="Michael Schumacher",
				first_name="Michael",
				last_name="Schumacher",
                email="Michael.Schumacher@gmail1.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=True)
md = models.SupplierUser(nickname="Max Designer",
				first_name="Max",
				last_name="Designer",
                email="Max.Designer@gmail1.com",
                password="12345678",
                last_seen=datetime.now(),
                receive_emails=False)
db.session.add(pb)
db.session.add(dn)
db.session.add(ase)
db.session.add(ms)
db.session.add(md)
db.session.commit()

# Add projects
project_auditory_test = models.Project(name="AD overtaking",
				description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent laoreet in ligula nec bibendum. Etiam bibendum enim sed urna vulputate, vel hendrerit purus tincidunt. In quis dui vitae mi porttitor auctor. Morbi tristique ipsum a orci maximus suscipit. Donec vestibulum sagittis nunc et venenatis. Quisque consectetur, nunc vel egestas condimentum, tellus tellus sagittis eros, sed tempus massa arcu vitae arcu. Praesent a viverra mi. Curabitur nisi sapien, gravida eu massa non, placerat finibus diam. Proin consectetur eget metus vitae placerat. Maecenas ligula lectus, feugiat vestibulum pellentesque ac, sagittis vel tortor.",
				filename="Description_project1.docx",
				finished=0,
				user=pb,
				timestamp=datetime.now())
db.session.add(project_auditory_test)
db.session.commit()

# Add assets
asset1 = models.Asset(name="Beep for left overtaking",
				description="Cras lacinia magna nisl. Sed maximus dui eros, eget feugiat ex vehicula a. Duis vestibulum, eros non eleifend venenatis, lorem nisi vehicula diam, sit amet dapibus nulla lacus vel elit.",
        		status=models.AssetStatus.iteration.value,
        		project=project_auditory_test,
        		finished=0,
        		iteration_number=0,
        		timestamp=datetime.now(),
        		notify_by_email=True)
asset2 = models.Asset(name="Beep for right overtaking",
				description="Cras lacinia magna nisl. Sed maximus dui eros, eget feugiat ex vehicula a. Duis vestibulum, eros non eleifend venenatis, lorem nisi vehicula diam, sit amet dapibus nulla lacus vel elit.",
                status=models.AssetStatus.iteration.value,
                project=project_auditory_test,
                finished=0,
                iteration_number=0,
                timestamp=datetime.now(),
                notify_by_email=True)
description1 = models.Description(duration="200",
				description="Cras lacinia magna nisl. Sed maximus dui eros, eget feugiat ex vehicula a. Duis vestibulum, eros non eleifend venenatis, lorem nisi vehicula diam, sit amet dapibus nulla lacus vel elit.",
        		sound_type=1,
                sound_family=1,
        		pitch="B#",
        		user=pb,
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
				description="Cras lacinia magna nisl. Sed maximus dui eros, eget feugiat ex vehicula a. Duis vestibulum, eros non eleifend venenatis, lorem nisi vehicula diam, sit amet dapibus nulla lacus vel elit.",
                sound_type=1,
                sound_family=1,
                pitch="A",
                user=pb,
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
asset1.client_add(pb)
asset1.client_add(sc)
asset1.supplier_add(sb)
asset1.supplier_add(jw)
asset2.client_add(pb)
asset2.supplier_add(sb)
asset1.init_in_hands()
asset2.init_in_hands()

project_auditory_test.asset_add(asset1)
project_auditory_test.asset_add(asset2)
db.session.commit()
