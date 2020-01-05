import React from 'react';
import { MODEL_FIELDS } from '../../utils/constants';
import fetchService from '../../utils/service';

export default class Model extends React.Component {
  constructor() {
    super();
    this.state = {
      trainedModels: null,
      modelFieldValues: {
        optimizer: '',
        learning_rate: '',
        learning_rate_decay: '',
        epochs: '',
        hidden_layer_sizes: '',
        layer_activations: '',
        layer_dropout_values: '',
        weight_initializers: '',
        batch_size: '',
      },
      isModelSent: false,
    };
  }

  componentDidMount() {
    fetchService('/api/models')
      .then((response) => {
        if (response.success) {
          this.setState({ trainedModels: response.data })
        }
      })
      .catch((error) => {
        if (!error.success) {
          alert(error.data);
        }
      });
  }

  handleFormValueChange = (e, fieldKey) => {
    e.preventDefault();
    const fieldValue = e.target.value.split(',')
    this.setState({
      modelFieldValues: {
        ...this.state.modelFieldValues,
        [fieldKey]: fieldValue.length > 1 ? fieldValue.map((item) => item.trim()) : fieldValue[0].trim(),
      }
    });
  }

  fillFormWithDefaultValues = (e) => {
    e.preventDefault();
    let { modelFieldValues } = this.state;

    MODEL_FIELDS.forEach((field) => {
      if (modelFieldValues[field.key] === '') {
        modelFieldValues[field.key] = field.defaultValue;
      }
    })

    this.handleFormSubmit(modelFieldValues)
  }

  handleFormSubmit = (modelFieldValues) => {
    fetchService('/api/train', 'POST', modelFieldValues)
      .then((response) => {
        if (response.success) {
          this.setState({ isModelSent: true });
        }
      })
      .catch((error) => {
        if (!error.success) {
          alert(error);
          this.setState({ isModelSent: false });
        }
      });
  }

  render() {
    const { trainedModels, modelFieldValues, isModelSent } = this.state;

    return (
      <div className="container">
        <div className="row mb-3">
          <div className="col-6">
            <h3>Trained models</h3>
            <div>
              {trainedModels && trainedModels.map((model, index) => (
                <div key={model.model_name + index}>
                  <div className="row">
                    <div className="col-12">
                      <h4><i>{model.model_name}</i></h4>
                      <p>Training time: {model.configuration.training_time}</p>
                    </div>
                    {Object.keys(model.configuration.train_parameters).map((param, index) => (
                      <div className="col-auto" key={index}>
                        <p>{param}: {model.configuration.train_parameters[param].toString()}</p>
                      </div>
                    ))}
                  </div>
                  <hr />
                </div>
              ))}
            </div>
          </div>
          <div className="col-6">
            <h3>Train new model</h3>
            <form className="mb-3" onSubmit={this.fillFormWithDefaultValues}>
              {
                MODEL_FIELDS.map((field, index) => (
                  <div className="form-group row" key={field.key + index}>
                    <label
                      className="col-5 col-form-label"
                      htmlFor={field.key}
                    >
                      {field.name}
                    </label>
                    <div className="col-7">
                      <input
                        className="form-control"
                        id={field.key}
                        type={field.type}
                        value={modelFieldValues[field.key]}
                        placeholder={field.defaultValue}
                        onChange={(e) => this.handleFormValueChange(e, field.key)}
                      />
                    </div>
                  </div>
                ))
              }
              <button className="btn btn-primary" type="submit">Submit</button>
            </form>
            <div className={!isModelSent ? 'd-none' : ''}>Model successfully sent!</div>
          </div>
        </div>
      </div>
    );
  }
}
