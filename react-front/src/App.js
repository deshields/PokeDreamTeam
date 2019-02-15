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
  deleteA(id){
  var ind = 0;
  this.AList.setState(prevState => ({
      items: prevState.items.filter(el => el != id ),
      ind: prevState.items.filter( function (el) {
        if(el != id) {
          return el.index;
        }
      })

   })



  );
 }

   trueSubmissonA = (event)=>{
    if(this.state.ATeam.length < 6){
      this.setState({
        ATeam: ATeam.concat(this.Pa.handleSubmit())
      })
      const newMember = {
        index: this.state.ATeam.length - 1,
        all: this.Pa.getData(),
        sprite: this.Pa.getData().sprite,
        text: this.Pa.getData().name
      }
      if(this.AList.state.items.length < 6){
        this.AList.setState(state =>({
            items: state.items.concat([newMember]),
          })
        )
      }

    }
  }

   trueSubmissonB =(event)=>{
       if(this.state.BTeam.length < 6){
       this.setState({
         BTeam: BTeam.concat(this.Pb.handleSubmit())
       })

       const newMember = {
         index: this.state.BTeam.length - 1,
         all: this.Pb.getData(),
         sprite: this.Pb.getData().sprite,
         text: this.Pb.getData().name

       }
       if(this.BList.state.items.length < 6){
         this.BList.setState(state =>({
             items: state.items.concat(newMember),
           })
         )
       }

     }
   }

  render() {
    return (
      <div className="App">


        <div className='pokemonInput'>
          <div className='Team'>
            <Playerform side={'A'} team={this.state.ATeam} ref={(ref) => this.AList = ref}/>
            <div className='pokeform'>
            <PokeAuto side={'A'} ref={(ref) => this.Pa = ref}/>
            <button value="Add to Team A" onClick={this.trueSubmissonA}> Add to Team! </button>
            </div>
          </div>
          <div className='Team'>
            <Playerform side={'B'} team={this.state.BTeam} ref={(ref) => this.BList = ref}/>
            <div className='pokeform'>
            <PokeAuto side={'B'} ref={(ref) => this.Pb = ref}/>
            <button value="Add to Team B" onClick={this.trueSubmissonB}> Add to Team! </button>
            </div>
          </div>
        </div>
        <div className='log'>
        <h3><i><u> BATTLE LOG </u></i></h3>

        </div>
      </div>
    );
  }
}



export default App;
