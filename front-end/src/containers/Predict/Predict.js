import React from 'react';
import csvParser from 'papaparse';
import { fetchService } from '../../utils';
import { Spinner } from 'react-bootstrap';
import './style.scss';

export default class Predict extends React.Component {
  constructor() {
    super();
    this.state = {
      isPending: false,
      predictions: []
    };
  }

  parseCSVData = (parsedCSV) => {
    const predictModelData = {};
    //fill predictModel with keys and values;
    parsedCSV.data[0].forEach((key, index) => {
      predictModelData[key] = [];
      parsedCSV.data.forEach((array, jindex) => {
        if (jindex === 0) return;
        if (array[index]) {
          predictModelData[key].push(array[index]);
        }
      });
    });

    return predictModelData;
  }

  postCSVData = (predictModelData) => {
    this.setState({ isPending: true });
    fetchService('/api/predict', 'POST', predictModelData)
      .then((response) => {
        let predictions = [];
        if (response.success) {
          predictions = response.data;
        }
        this.setState({ isPending: false, predictions });
      }).catch((error) => {
        alert(error);
        this.setState({ isPending: false });
      });
  }

  onImportCSVClick = (evt) => {
    const reader = new FileReader();
    reader.onload = (_evt) => {
      const parsedCSV = csvParser.parse(_evt.target.result);
      const predictModelData = this.parseCSVData(parsedCSV);

      if (parsedCSV.errors.length) {
        alert("CSV ERRORS");
        return;
      }
      this.postCSVData(predictModelData);
    };
    reader.readAsText(evt.target.files[0]);
  };

  render() {
    const { isPending, predictions } = this.state;
    console.log(predictions);

    if (isPending) {
      return (
        < Spinner animation="border" />
      )
    }

    return (
      <div className="container predict">
        <div className="mt-3 row">
          <div className="col">
            <button type="button" className="app-button">
              <input
                type="file"
                id="selectFiles"
                accept=".csv"
                onChange={this.onImportCSVClick}
              />
            </button>
          </div >
        </div >
        <div className="mt-3 row flex-column justify-content-center">
          <h1>Prediction</h1>
          <div className="col-10 mt-1 p-4 predictions">
            {predictions}
          </div>
        </div>
      </div>
    );
  }
}
