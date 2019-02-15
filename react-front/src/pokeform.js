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

var levelnum = 1

class PokeAuto extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      value: '',
      onSubmit: this.handleSubmit,
      suggestions: [],
      lvl: 1,
      side: '',
      // form: '',
      poke: 'Pikachu',
      move1: '',
      move2: '',
      move3: '',
      move4: '',
      };
    };

  handleChange(event) {
  this.setState({value: event.target.value});
};

  getData = () => {
    return {"sprite": Pokemon.getSprite(this.state.poke), "name": this.state.poke, "side": this.props.side, "level": this.state.lvl, "move1": this.state.move1, "move2": this.state.move2, "move3": this.state.move3, "move4": this.state.move4}
  }

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

  numChange(num) {
    levelnum = num
    return num
  }


  handleSubmit = () => {
    this.setState({
      move1: this.move_1.getMoveData(),
      move2: this.move_2.getMoveData(),
      move3: this.move_3.getMoveData(),
      move4: this.move_4.getMoveData(),
      lvl: levelnum
    }, function () {
      return this.getData()

    });
  }

  render() {
    const { value, suggestions } = this.state;
    const pokeProp = {
      placeholder: 'Enter a Valid Species',
      value,
      onChange: this.onChange
    };
    const suggestedPokemon = getSuggestionValue

    return(
      <div>


        <Autosuggest
          id={'PokemonName'}
          suggestions={suggestions}
          onSuggestionsFetchRequested={this.onPokeSuggestionsFetchRequested}
          onSuggestionsClearRequested={this.onSuggestionsClearRequested}
          getSuggestionValue={getSuggestionValue}
          renderSuggestion={renderSuggestion}
          inputProps={pokeProp}
        />

        <img src={Pokemon.getSprite(this.state.poke)} className={'spriteImg'} alt=""/>


        <NumericInput mobile min={1} max={100} strict className="lvl" id="lvl" placeholder="Enter level." format={this.numChange}/>

        <div className='moves'>
          <table>
          <tr>
            <td><MoveAuto id={'move1'} ref={(ref) => this.move_1 = ref}/> </td>
            <td><MoveAuto id={'move2'} ref={(ref) => this.move_2 = ref}/> </td>

          </tr> <tr>
            <td><MoveAuto id={'move3'} ref={(ref) => this.move_3 = ref}/></td>
            <td><MoveAuto id={'move4'} ref={(ref) => this.move_4 = ref}/></td>
            </tr>
          </table>

        </div>

    </div>
    );

  } 

}
export default PokeAuto;
