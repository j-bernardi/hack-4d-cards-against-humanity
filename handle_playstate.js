//document.getElementById('question-div')
//document.getElementById('card-div')

document.getElementById('run-script-button').onclick = runScript;

var ai_answer;
var final_human_answer;
var question;

function get_question() {
  var self = this;
  this.question = "empty";
  $.ajax({
    async: false,
    url: 'http://localhost:5000/geta-question',
    success: function(data){
		    //data.result is returned by the jsonify in the python script
          self.question = data.question;
          document.getElementById('question-text').innerHTML = data.question;
    }
  });
  return this.question
};

function get_ai_answer(){
  var self = this;
  this.answer = "empty";
  $.ajax({
    async: false,
    url: 'http://localhost:5000/play/' + (question.split(" ")).join("|"),
    success: function(data){
      self.answer = data.ai_answer
    }
  });
  return this.answer
}

function get_answers(){
  var self = this;
  this.answers = "empty";
  $.ajax({
    async: false,
    url: 'http://localhost:5000/play/' + (question.split(" ")).join("|"),
    success: function(data){
		  //data.result is returned by the jsonify in the python script
      self.answers = data.answers
      document.getElementById('card-div').innerHTML = generateButtons(data.answers);

	  }
  });
  return this.answers
}

function generateButtons(answers){
  var prefix = "<button class='card-button' id='card";
  var mid = "onClick='card_selected(this.id)'>"
  var suffix = "</button>";

  var ansLst = answers.split("|");
  var line = "";

  var lineLst = new Array(ansLst.length);

  for (i=0; i<ansLst.length; i++){

    line = prefix + String(i+1) + "'" + mid + ansLst[i] + suffix;
    lineLst[i] = line;
  }

  return lineLst.join("\t")
}

function card_selected(card_id){

  var elem = document.getElementById(card_id);

  var answer = elem.firstChild.nodeValue;

  final_human_answer = answer

  document.getElementById("vote-div").innerHTML = "<h2>Pick your favourite</h2>\n \
    <button id='human_button' onClick=voteSelected('human')>" + question.replace("_", answer) + "</button>\n" +
    "<button id='ai_button' onClick=voteSelected('ai')>" + ai_answer + "</button>"
}

function get_scores(human_phrase, ai_phrase){

  var self = this;
  this.answers = "empty";
  $.ajax({
    async: false,
    url: 'http://localhost:5000/analyse/' + human_phrase.split(" ").join("|") + "+" + ai_phrase.split(" ").join("|"),
    success: function(result){
		  //data.result is returned by the jsonify in the python script
      self.amazon_human_score = result.amazon_human_score
      self.azure_human_score = result.azure_human_score

      self.amazon_ai_score = result.amazon_ai_score
      self.azure_ai_score = result.azure_ai_score

	  }
  });
  return [this.amazon_human_score, this.azure_human_score, this.amazon_ai_score, this.azure_ai_score]
}

function voteSelected(winner){
  return_string = "<h2> winner is " +
    winner.toUpperCase() + "!!!</h2>"

  scores = get_scores(final_human_answer, ai_answer);
  am_h = scores[0]
  az_h = scores[1]
  am_a = scores[2]
  az_a = scores[3]
  return_string += "<p>"
  return_string += "Amazon rated your answer: " + am_h + "<br>"
  return_string += "Microsoft Azure rated your answer: " + az_h + "<br>"

  return_string += "Amazon rated the bot's answer " + am_a + "<br>"
  return_string += "Microsoft Azure rated the bot's answer " + az_a + "<br>"
  return_string += "</p>"

  document.getElementById("winner-div").innerHTML = return_string


}

function runScript(){

	console.log('running script')

  //The qquestion of the current state
  question = get_question();
  console.log("Question: "  + question)

  // The answers available to the human
  var answer_string = get_answers();
  var answers = answer_string.split("|");

  // the answer that's been pre-selected by the robot
  ai_answer = get_ai_answer();
  console.log("Ai answer: " + ai_answer)

}
