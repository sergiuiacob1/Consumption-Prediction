# Consumption Prediction

## Requirement (in Romanian)
Predicția consumului de energie
- Înțelegerea setului de date: crea unor grafice care sa ilustreze corelații între parametri, înțelegerea anumitor biasuri care apar în setul de date etc. Se va acorda bonus pentru găsirea unor interpretări originale ale datelor.
- Identificarea și eliminarea instanțelor aberante din setul de date.
- Scalarea (normalizarea) datelor din fiecare coloana (unde e cazul) la același interval pentru ca toate feature-uri să contribui în aceeași masura la rezultatul predicției.
- Crearea unei rețele neuronale care sa prezica consumul de curent (coloana Consumptia_MW). Evaluarea calității predicțiilor se va face folosind Mean squared error. Se acorda bonus pentru obținerea unui scor MSE < 600.

## App Architecture
| Team Members | Component Name | Component Description | Deadline |
| ------------ | -------------- | --------------------- | -------- |
| Serban Cobzac, Cristi Ginju | Statistics | Graphics for data analysis | 16th of January, 2020 |
| Radu Stan  | Dashboard  | Create the app dashboard + back-end connection, Heroku Deploy | 16th of January, 2020 |
| Iacob Sergiu, Medvichi Stefan  | Back-end  | Normalize data, train model, predict | 9th of January, 2020 |
