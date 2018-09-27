import Autosuggest from 'react-autosuggest';
import React, { Component } from 'react';
import moveNames from './moveNames.js'

const getMoveSuggestions = value => {
  const inputValue = value.trim().toLowerCase();
  const inputLength = inputValue.length;

  return inputLength === 0 ? [] : moveNames.filter(move =>
    move.name.toLowerCase().slice(0, inputLength) === inputValue
  );
};


const getSuggestionValue = suggestion => suggestion.name;

const renderSuggestion = suggestion => (
  <div>
    {suggestion.name}
  </div>
);

class MoveAuto extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      value: '',
      suggestions: [],
      form: '',
      id: '',
    };
  }

  onChange = (event, {newValue}) => {
    this.setState({
      value: newValue
    });
  };

  onMoveSuggestionsFetchRequested = ({ value }) => {
    this.setState({
      suggestions: getMoveSuggestions(value)
    });
  };

  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });

  };

  render() {
    const { value, suggestions } = this.state;

    const moveProps = {
      placeholder: 'Enter a Move',
      value,
      onChange: this.onChange
    };


    return(
      <Autosuggest
        id={this.state.id}
        suggestions={suggestions}
        onSuggestionsFetchRequested={this.onMoveSuggestionsFetchRequested}
        onSuggestionsClearRequested={this.onSuggestionsClearRequested}
        getSuggestionValue={getSuggestionValue}
        renderSuggestion={renderSuggestion}
        inputProps={moveProps}
      />

    );

  }

}
export default MoveAuto;
