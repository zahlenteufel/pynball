import math

standard = {
    'size': {'width': 400, 'height': 600},
    'ball': {
        'radius': 10,
        'position': (160, 510),
        'velocity': (0, 0)
    },
    'gravity': 0,
    'obstacles': [
        {'from': (318, 464), 'to': (256, 518)},
        {'from': (319, 354), 'to': (318, 464)},

        {'from': (72, 359), 'to': (72, 430)},

        {'from': (40, 357), 'to': (40, 438)},
        {'from': (40, 438), 'to': (140, 519)},

        {'from': (43, 505), 'to': (131, 576)},
        {'from': (131, 576), 'to': (131, 603)},

        {'from': (295, 603), 'to': (295, 550)},
        {'from': (295, 550), 'to': (354, 487)},

        {'from': (101, 359), 'to': (148, 472)},
        {'from': (148, 472), 'to': (101, 434)},
        {'from': (101, 434), 'to': (101, 359)},

        {'from': (279, 359), 'to': (279, 450)},
        {'from': (279, 450), 'to': (251, 479)},
        {'from': (251, 479), 'to': (279, 359)}
    ],
    'fingers': [
        {
            'type': 'L',
            'pivot': (140, 530),
            'length': 50,
            'r1': 11,
            'r2': 6,
            'min_angle': -math.pi / 4,
            'max_angle': math.pi / 4,
            'color': (255, 0, 0)
        },
        {
            'type': 'L',
            'pivot': (260, 530),
            'length': 45,
            'r1': 11,
            'r2': 6,
            'min_angle': -math.pi / 4,
            'max_angle': math.pi / 4,
            'color': (0, 255, 0)
        }
    ]
}

debug_left_finger = {
    'size': {'width': 500, 'height': 500},
    'ball': {
        'radius': 30,
        'position': (210, 100),
        'velocity': (0, 0)
    },
    'gravity': 0,
    'obstacles': [],
    'fingers': [
        {
            'type': 'L',
            'r1': 50,
            'r2': 20,
            'pivot': (50, 250),
            'length': 300,
            'min_angle': -math.pi / 6,
            'max_angle': math.pi / 6,
            'color': (255, 0, 0)
        }
    ]
}
