from engine.combat_system import Attack, Heal, Spell, Combo

punch = Attack('punch',30)
kick = Attack('kick',15)
knee_smash = Attack('knee smash',30)

small_heal = Heal('small heal',10)
average_heal = Heal('average heal',30)
mega_heal = Heal('mega heal',50)

attack_dict = {

	'attacktype':{
		'punch':punch,
		'kick':kick,
		'knee_smash':knee_smash
	},

	'healtype':{
		'small_heal':small_heal,
		'average_heal':average_heal,
		'mega_heal':mega_heal,
	}

}

all_attacks = [punch,kick,knee_smash,small_heal,average_heal,mega_heal]


