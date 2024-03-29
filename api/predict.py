import pickle
import datetime
import pandas as pd


class Predictions:
    def __init__(self, model_name: str) -> None:
        """
        model name to be loaded for prediction
        """
        with open(
            rf"C:\Users\hp\Desktop\RedBuffer\Gold_Prices_task_1\models\{model_name}.pckl",
            "rb",
        ) as fin:
            try:
                self.model = pickle.load(fin)
            except OSError:
                print("wrong path/ model not available")
                exit(-1)

    def predict(self, prev_date: str):
        """
        Predicts gold prices for next date
        date_format = yyyy-mm-dd
        """
        self.next_date = datetime.datetime(
            *list(map(lambda x: int(x), prev_date.split("-")))
        ) + datetime.timedelta(
            days=1
        )  # next date

        # preprocess date

        next_date_series = pd.DataFrame(
            {"ds": pd.date_range(start=self.next_date, end=self.next_date)}
        )

        pred = self.model.predict(next_date_series)

        return pred

    def get_next_date(self):
        return self.next_date.strftime("%y-%m-%d")

    def plot(self, pred):
        self.model.plot(pred)


# testing
if __name__ == "__main__":
    pr = Predictions("fb_p")
    pred = pr.predict("2022-12-31")
    print(pred)
