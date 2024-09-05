def generate_suggestions(prediction):
    """
    Generate driving suggestions based on the prediction.
    The suggestions are based on the driving behavior and score.
    """
    behavior = prediction.get('behavior')
    score = prediction.get('score')

    if behavior == 'Aggressive':
        return [
            "Reduce sudden accelerations",
            "Avoid sharp turns and quick lane changes",
            "Maintain a steady speed to improve safety"
        ]
    elif behavior == 'Moderate':
        return [
            "Try to smooth out accelerations",
            "Drive smoothly to reduce moderate speed variations",
            "Maintain steady speed to improve driving score"
        ]
    elif behavior == 'Safe':
        return [
            "Excellent driving! Continue following traffic rules",
            "Maintain safe speeds and smooth driving"
        ]
    else:
        return [
            "Drive cautiously and avoid harsh maneuvers",
            "Follow traffic rules and maintain awareness"
        ]
