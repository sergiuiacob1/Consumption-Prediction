import React from 'react';
import { MODEL_FIELDS } from '../../utils/constants';
import fetchService from '../../utils/service';

export default class Model extends React.Component {
  constructor() {
    super();
    this.state = {
      trainedModels: null,
      modelFieldValues: {
        learning_rate: '',
        learning_rate_init: '',
        max_iter: '',
        tol: '',
        hidden_layer_sizes: '',
        batch_size: '',
        solver: '',
        activation: '',
      },
      isModelSent: false,
    };
  }

  componentDidMount() {
    fetchService('/api/models')
      .then((response) => {
        this.setState({ trainedModels: response.data.message })
      })
      .catch((error) => {
        alert(error);
      });
  }

  handleFormValueChange = (e, fieldKey) => {
    e.preventDefault();
    this.setState({
      modelFieldValues: {
        ...this.state.modelFieldValues,
        [fieldKey]: e.target.value,
      }
    });
  }

  handleFormSubmit = (e) => {
    e.preventDefault();
    const { modelFieldValues } = this.state;

    if (this.validateForm()) {
      fetchService('/api/train', 'POST', modelFieldValues)
        .then((response) => {
          if (response.success) {
            this.setState({ isModelSent: true });
          }
        })
        .catch((error) => {
          alert(error);
          this.setState({ isModelSent: false });
        });
    }
  }

  render() {
    const { trainedModels, modelFieldValues, isModelSent } = this.state;

    return (
      <div className="container">
        <div className="row mb-3">
          <div className="col-6">
            <h4>Trained models</h4>
            <div>{trainedModels}</div>
          </div>
          <div className="col-6">
            <h4>Train new model</h4>
            <form className="mb-3" onSubmit={this.handleFormSubmit}>
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
                        required
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
