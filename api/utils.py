import pickle
import datetime
from typing import List
import pandas as pd
from abc import ABC, abstractmethod


class GoldPricePredictor(ABC):
    def __init__(self, model_name) -> None:
        """
        Loads the model from the given file
        """
        with open(f"models/{model_name}.pckl", "rb",) as fin:
            try:
                self.model = pickle.load(fin)
            except (OSError, FileNotFoundError, TypeError):
                print("wrong path/ model not available")
                exit(-1)

    def calculate_next_date(self, prev_date):
        """
        Calculates next date
        date_format = yyyy-mm-dd
        """
        self.next_date = datetime.datetime(
            *list(map(lambda x: int(x), prev_date.split("-")))
        ) + datetime.timedelta(
            days=1
        )  # next date

    def get_next_date(self, prev_date):
        try:
            return self.next_date.strftime("%y-%m-%d")
        except NameError:
            self.calculate_next_date(prev_date)

    @abstractmethod
    def predict(self, prev_date) -> List:
        pass

    @abstractmethod
    def preprocess_inputs(self, prev_date):
        pass

    @abstractmethod
    def postprocess_outputs(self, output_from_model) -> List:
        pass


class ArimaPredictor(GoldPricePredictor):
    def __init__(self) -> None:
        """
        Load the model from the file models/auto_arima.pckl
        """
        super().__init__("auto_arima")

    def preprocess_inputs(self, prev_date):
        super().calculate_next_date(prev_date)

    def postprocess_outputs(self, output_from_model) -> List:
        return output_from_model.tolist()

    def predict(self, prev_date):
        self.preprocess_inputs(prev_date)
        pred = self.model.forecast(prev_date)
        pred = self.postprocess_outputs(pred)
        return pred


class FBProphetPredictor(GoldPricePredictor):
    def __init__(self,) -> None:
        """
        Load the Model from file models/fbprophet.pckl
        """
        super().__init__("fbprophet")

    def preprocess_inputs(self, prev_date):
        """
        Model takes in an input which is a pandas dataframe having index 
        as the day to be predicted
        """
        self.calculate_next_date(prev_date)  # get the self.next_date var
        next_date_series = pd.DataFrame(
            {"ds": pd.date_range(start=self.next_date, end=self.next_date)}
        )
        return next_date_series

    def postprocess_outputs(self, output_from_model) -> List:
        """
        Return the yhat in the list format
        """
        return output_from_model["yhat"].tolist()

    def predict(self, prev_date) -> List:
        next_date_series = self.preprocess_inputs(prev_date)  # preprocess inp

        pred = self.model.predict(next_date_series)  # prediction

        pred = self.postprocess_outputs(pred)  # postprocess prediction
        return pred  # return prediction


# testing
if __name__ == "__main__":
    # pr = Predictions("fb_p")
    # pred = pr.predict("2022-12-31")
    # print(pred)
    pass
