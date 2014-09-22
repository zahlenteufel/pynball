import math

standard = {
    'size': {'width': 400, 'height': 600},
    'ball': {
        'radius': 10,
        'position': (160, 520),
        'velocity': (0, 0)
    },
    'gravity': 0,
    'obstacles': [
        {'from': (50, 450), 'to': (140, 530)},
        {'from': (260, 530), 'to': (320, 475)}
    ],
    'fingers': [
        {
            'type': 'L',
            'pivot': (140, 540),
            'length': 40,
            'min_angle': -math.pi / 4,
            'max_angle': math.pi / 4,
            'color': (255, 0, 0)
        },
        {
            'type': 'R',
            'pivot': (260, 540),
            'length': 40,
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
