def get_max_score_model(models, X_test, y_test):
    max_score, best_model = 0, None

    for model in models:
        score = model.score(X_test, y_test)
        print('- {}: {:.4f}'.format(type(model).__name__, score))
        if score > max_score:
            max_score, best_model = score, model

    return max_score, best_model