import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Autosuggest from 'react-autosuggest';
import PokeAuto from './pokeform.js';
import MoveAuto from './moveform.js';
import Playerform from './Playerform.js';



const ATeam = []
const BTeam = []
class App extends Component {
  constructor(){
    super();
    this.state = {
      ATeam: [],
      BTeam: []
    }
  }

   trueSubmissonA = (event)=>{
    if(this.state.ATeam.length < 6){
      this.setState({
        ATeam: ATeam.concat(this.Pa.handleSubmit())
      })
      const newMember = {
        sprite: this.Pa.getData().sprite,
        text: this.Pa.getData().name

      }
      this.AList.setState(state =>({
          items: state.items.concat([newMember]),
        })
      )

    }
  }

   trueSubmissonB =(event)=>{
       if(this.state.BTeam.length < 6){
       this.setState({
         BTeam: BTeam.concat(this.Pb.handleSubmit())
       })

       const newMember = {
         sprite: this.Pb.getData().sprite,
         text: this.Pb.getData().name

       }
       this.BList.setState(state =>({
           items: state.items.concat(newMember),
         })
       )

     }
   }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>

        <Playerform side={'A'} team={this.state.ATeam} ref={(ref) => this.AList = ref}/>

        <div className='pokemonInput'>
        <div className='pokeform'>
        <PokeAuto side={'A'} ref={(ref) => this.Pa = ref}/>
        <button value="Add to Team A" onClick={this.trueSubmissonA}/>
        </div>

        <Playerform side={'B'} team={this.state.BTeam} ref={(ref) => this.BList = ref}/>
        <div className='pokeform'>
        <PokeAuto side={'B'} ref={(ref) => this.Pb = ref}/>
        <button value="Add to Team B" onClick={this.trueSubmissonB}/>
        </div>


        </div>
      </div>
    );
  }
}



export default App;
