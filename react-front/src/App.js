import React, { Component } from 'react';
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
        text: this.Pa.getData().name,
        // team: "A",
        // trainer: "Red"
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
         // sprite: this.Pb.getData().sprite,
         // text: this.Pb.getData().name,
         // team: "B",
         // trainer: "Blue"

       }
       if(this.BList.state.items.length < 6){
         this.BList.setState(state =>({
             items: state.items.concat(newMember),
           })
         )
       }

     }
   }


    convertToJsonStr(trainer, side, team){
      var list = [];
      for (const [index, value] of team.entries()){
        list.push(value);
      }
      console.log(list)
      let ret = {'trainer': trainer, 'side': side, "team":list}
      return ret;

    }

    convertTeamsToJsonStr=()=>{
      var list = [];
      list.push(this.convertToJsonStr("Red", "A", this.AList.state.items));
      list.push(this.convertToJsonStr("Blue", "B", this.BList.state.items));
      // console.log(this.AList.state.items) //pass
      console.log(list) //fail
      return list;
    }

    sendJSONthroughServer=()=>{
      // e.preventDefault();
      let xhr = new XMLHttpRequest();
      xhr.open('POST', 'http://127.0.0.1:5000/run')
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      console.log(this.convertTeamsToJsonStr()) // failed
      xhr.send(JSON.stringify(this.convertTeamsToJsonStr()))
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
          <form id="to-battle" onSubmit={this.sendJSONthroughServer}>
            <button> Battle! </button>
          </form>
        </div>

        <div className='log'>
        <h3><i><u> BATTLE LOG </u></i></h3>

        </div>
      </div>
    );
  }
}



export default App;
