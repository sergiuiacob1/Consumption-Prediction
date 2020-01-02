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
      formData: {
        "Date": [],
        "Coal_MW": [],
        "Gas_MW": [],
        "Hidroelectric_MW": [],
        "Nuclear_MW": [],
        "Wind_MW": [],
        "Solar_MW": [],
        "Biomass_MW": [],
        "Production_MW": [],
      },
      fillFormData: false,
      noOfFormData: 1,
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

  onFormInputChange = (evt, key, index) => {
    const _state = this.state;
    _state.formData[key][index] = evt.target.value;
    this.setState(_state);
  }

  changeRowNumbers = (noOfFormData) => {
    this.setState({ noOfFormData });
  }


  renderForm = () => {
    const { formData, noOfFormData, fillFormData } = this.state;
    return (
      <div className="predict-form">
        {[...Array(noOfFormData)].map((x, index) => (
          <div className="d-flex mb-5" key={index}>
            {Object.keys(formData).map((key) => {
              return (
                <div key={key} >
                  <h6>{key}</h6>
                  <div className="mr-5">
                    <input
                      key={`${key}${index}`}
                      type="text"
                      className="form-control"
                      placeholder={key}
                      aria-label={key}
                      onChange={(evt) => this.onFormInputChange(evt, key, index)}
                      value={formData[key][index] || ''}
                      disabled={!fillFormData}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        ))}
        <div className="">
          <button
            type="button"
            className="btn btn-primary mr-3"
            onClick={() => this.changeRowNumbers(noOfFormData + 1)}
          >
            New entry row
          </button>
          <button
            type="button"
            className="btn btn-danger mr-3"
            disabled={noOfFormData < 2}
            onClick={() => this.changeRowNumbers(noOfFormData - 1)}
          >
            Delete row
            </button>
          <button
            type="button"
            className="btn btn-success mr-3"
            onClick={() => this.postCSVData(formData)}
          >
            Submit data
            </button>
        </div>
      </div>
    )
  }

  onFillFormDataClick = () => {
    this.setState({ fillFormData: !this.state.fillFormData })
  }

  render() {
    const { isPending, predictions, fillFormData, } = this.state;

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
          </div>
        </div>
        <div>
          <h2 className="my-3">OR</h2>
          <label className="d-flex align-items-center" htmlFor="fill-form-data" onClick={this.onFillFormDataClick}>
            <input type="checkbox" name="fill-form-data" checked={fillFormData} />
            <h5 className="ml-2">Enter your data</h5>
          </label>
        </div>
        <div className="mt-3 row">
          <div className="col">
            {this.renderForm()}
          </div>
        </div>
        <div className="mt-3 row flex-column justify-content-center">
          <h1>Prediction</h1>
          <div className="col-10 mt-1 p-4 predictions">
            {predictions.map((prediction, index) => (<div> <b>Index {index + 1}:</b> {prediction}</div>))}
          </div>
        </div>
      </div >
    );
  }
}
