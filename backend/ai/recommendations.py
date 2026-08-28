def generate_recommendations(
    matched_skills: list[str],
    missing_skills: list[str]
) -> list[str]:

    recommendations = []

    if matched_skills:
        recommendations.append(
            "Highlight your matched skills prominently in your resume, "
            "especially in the skills, projects, and experience sections."
        )

    if missing_skills:
        top_missing = missing_skills[:5]

        recommendations.append(
            "Consider learning or demonstrating these missing skills: "
            + ", ".join(top_missing)
            + "."
        )

    if len(matched_skills) < 3:
        recommendations.append(
            "Add more relevant technical skills and projects that closely "
            "match the target job description."
        )

    recommendations.append(
        "Use measurable achievements in your experience section, such as "
        "percent improvements, users served, revenue generated, or time saved."
    )

    recommendations.append(
        "Use keywords from the job description naturally throughout your resume."
    )

    return recommendations


def generate_learning_roadmap(
    missing_skills: list[str]
) -> list[str]:

    if not missing_skills:
        return [
            "Continue strengthening your current skills.",
            "Build projects that demonstrate your strongest technologies.",
            "Prepare examples of your work for technical interviews.",
        ]

    roadmap = []

    for skill in missing_skills[:5]:
        roadmap.append(
            f"Learn the fundamentals of {skill.title()} and build "
            f"a small practical project using it."
        )

    return roadmap