import React from 'react';
import csvParser from 'papaparse';
import { fetchService } from '../../utils';
import { Spinner } from 'react-bootstrap';
import './Predict.scss';

export default class Predict extends React.Component {
  constructor() {
    super();
    this.state = {
      isPending: false,
      formData: {
        "Date": [],
        "Coal": [],
        "Gas": [],
        "Hidroelectric": [],
        "Nuclear": [],
        "Wind": [],
        "Solar": [],
        "Biomass": [],
        "Production": [],
      },
      fillFormData: false,
      noOfFormData: 1,
      predictions: [],
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
      })
      .catch((error) => {
        debugger
        if (!error.success) {
          alert(error.data);
        }
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
      <form className="predict-form" onSubmit={() => this.postCSVData(formData)}>
        {[...Array(noOfFormData)].map((x, index) => (
          <div className="d-flex mb-4" key={index}>
            {Object.keys(formData).map((key) => {
              return (
                <div key={key} >
                  <h6>{key}</h6>
                  <div className="mr-3">
                    <input
                      key={`${key}${index}`}
                      type="text"
                      className="form-control"
                      placeholder={key === 'Date' ? 'timestamp' : 'MW value'}
                      aria-label={key}
                      onChange={(evt) => this.onFormInputChange(evt, key, index)}
                      value={formData[key][index] || ''}
                      disabled={!fillFormData}
                      required
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
            disabled={!fillFormData}
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
            type="submit"
            className="btn btn-success mr-3"
            disabled={!fillFormData}
          >
            Submit data
            </button>
        </div>
      </form>
    )
  }

  onFillFormDataClick = () => {
    this.setState({ fillFormData: !this.state.fillFormData })
  }

  render() {
    const { isPending, predictions, fillFormData, } = this.state;

    if (isPending) {
      return (
        <div className="container">
          <div className="row mb-3">
            <div className="col d-flex justify-content-center">
              <Spinner animation="border" />
            </div>
          </div>
        </div >
      )
    }

    return (
      <div className="container">
        <div className="row mb-3">
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
        <div className="row mb-3">
          <div className="col-12">
            <h4>OR</h4>
          </div>
          <div className="col-12">
            <label className="d-flex align-items-center" htmlFor="fill-form-data" onClick={this.onFillFormDataClick}>
              <input type="checkbox" name="fill-form-data" checked={fillFormData} onChange={this.onFillFormDataClick} />
              <h5 className="ml-2 mb-0">Enter your data</h5>
            </label>
          </div>
        </div>
        <div className="row mb-3">
          <div className="col">
            {this.renderForm()}
          </div>
        </div>
        <hr />
        <div className="row">
          <div className="col-12">
            <h1>Prediction</h1>
          </div>
          <div className="col-12 predictions">
            <div className="row">
              {predictions.length > 0
                ? predictions.map((prediction, index) => (<div className="col-auto"> <b>Index {index + 1}:</b> {prediction}</div>))
                : <div className="col">No data entered</div>
              }
            </div>
          </div>
        </div>
      </div >
    );
  }
}
