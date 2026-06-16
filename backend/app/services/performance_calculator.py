def calculate_scores(
    quantity_completed,
    duration_minutes,
    quality_percent,
    standard_quantity,
    standard_duration,
    standard_quality
):

    quantity_completed = float(quantity_completed)
    duration_minutes = float(duration_minutes)
    quality_percent = float(quality_percent)

    standard_quantity = float(standard_quantity)
    standard_duration = float(standard_duration)
    standard_quality = float(standard_quality)

    quantity_score = (
        quantity_completed
        / standard_quantity
    ) * 100

    time_score = (
        standard_duration
        / duration_minutes
    ) * 100

    quality_score = (
        quality_percent
        / standard_quality
    ) * 100

    final_score = (
        quantity_score
        + time_score
        + quality_score
    ) / 3

    return {
        "quantity_score": round(quantity_score, 2),
        "time_score": round(time_score, 2),
        "quality_score": round(quality_score, 2),
        "final_score": round(final_score, 2)
    }