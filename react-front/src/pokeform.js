import Autosuggest from 'react-autosuggest';
import NumericInput from 'react-numeric-input';
// import InputNumber from 'rc-input-number';
import Pokemon from 'pokemon-images';
import React, { Component } from 'react';
import Pokenames from './pokenames.js'
import MoveAuto from './moveform.js';

const getPokeSuggestions = value => {
  const inputValue = value.trim().toLowerCase();
  const inputLength = inputValue.length;

  return inputLength === 0 ? [] : Pokenames.filter(poke =>
    poke.name.toLowerCase().slice(0, inputLength) === inputValue
  );
};


const getSuggestionValue = suggestion => suggestion.name;

const renderSuggestion = suggestion => (
  <div>
    {suggestion.name}
  </div>
);

class PokeAuto extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      value: '',
      suggestions: [],
      lvl: 1,
      side: '',
      form: '',
      poke: 'Pikachu',
      move1: ''
      };
    };

  handleChange(event) {
  this.setState({value: event.target.value});
};

// handleLvlChange(event) {
//   this.setState( state => ({
//       lvl: state.lvl + 1
//     })
// }

  onChange = (event, {newValue, method}) => {
    this.setState({
      value: newValue
    });
    if (method === 'enter' || method === 'click'){
    this.setState({poke: newValue});
    }
  };


  onPokeSuggestionsFetchRequested = ({ value }) => {
    this.setState({
      suggestions: getPokeSuggestions(value)
    });
  };

  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });

  };

  render() {
    const { value, suggestions } = this.state;
    const pokeProp = {
      placeholder: 'Enter a Valid Species',
      value,
      onChange: this.onChange
    };
    const suggestedPokemon = getSuggestionValue

    return(
      <div className='pokeform'>

        <Autosuggest
          id={'PokemonName'}
          suggestions={suggestions}
          onSuggestionsFetchRequested={this.onPokeSuggestionsFetchRequested}
          onSuggestionsClearRequested={this.onSuggestionsClearRequested}
          getSuggestionValue={getSuggestionValue}
          renderSuggestion={renderSuggestion}
          inputProps={pokeProp}
        />

        <img src={Pokemon.getSprite(this.state.poke)} className={'spriteImg'}/>


        <NumericInput mobile min={1} max={100} strict className="lvl" id= "lvl" placeholder="Enter level."/>

        <div className='moves'>
          <table>
          <tr>
            <td><MoveAuto id={'move1'}/> </td>
            <td><MoveAuto id={'move2'}/> </td>

          </tr> <tr>
            <td> <MoveAuto id={'move3'}/></td>
            <td><MoveAuto id={'move4'}/></td>
            </tr>
          </table>

        </div>

    </div>
    );

  }

}
export default PokeAuto;
