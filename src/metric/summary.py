# Funciones usada para detectar missing values.

def missing_values_summary(df):
    result = round(df.isna().sum() * 100 / len(df), 2)
    result = result[result > 0]
    result = result.apply(lambda value: f'{value}%')
    return result

# Funciones utilizadas para contruir un resumen de datos relevante de un objeto SetsGroup.

def set_summary(features, target, title=None):
    if title:
        print(f'\n{title}:')
    print('- Features shape:',  features.shape)
    print('- Target shape:',     target.shape)
    print('- Target classes:')
    classes = target.value_counts(normalize=True)

    for index in range(0, len(classes) - 1):
        print("\t- Clase '{}': {:.2f} %".format(str(classes.index[index][0]), classes.values[index]* 100))
  
    missing = missing_values_summary(features)

    if missing.empty:
        print('- Valores faltantes en features: No hay valores faltantes!')
    else:
        print('- Valores faltantes en features: ')
        print(missing)