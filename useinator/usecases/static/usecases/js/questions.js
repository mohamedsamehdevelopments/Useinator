var caseForm = document.getElementById("case-form");
var nextBtn = document.getElementById("next-btn");
var btnContainer = document.getElementById("btn-container");
var count = 0;
var gBtn;
var bDiv;

var questions = [
	{
		name : "q1",
		type : "radio",
		label : "Is your system is automated online advising?",
		answer : ["Yes", "No"],
		aId : ["q1a1", "q1a2"]
	},

	{
		name : "q2",
		type : "radio",
		label : "Does your system depend on credit or semester?",
		answer : ["Credit", "Semester"],
		aId : ["q2a1", "q2a2"]
	},
	{
		name : "q3",
		type : "radio",
		label : "Does your system depend on gpa  or percentage?",
		answer : ["GPA", "Percentage?"],
		aId : ["q3a1", "q3a2"]
	},
	{
		name : "q4",
		type : "checkbox",
		label : "Please check type of constrains?",
		answer : ["Financial issue", "Major and concentration", "Limitation of course"],
		aId : ["q4a1", "q4a2", "q4a3"]
	},
	{
		name : "q5",
		type : "checkbox",
		label : "Who can authorize the system?",
		answer : ["Academics", "Admin", "finance"],
		aId : ["q5a1", "q5a2", "q5a3"]
	}
];
if(count === 0) {
	nextBtn.innerHTML = "Start";
}
nextBtn.addEventListener("click", function() {

	if (questions.length > count) {
		nextBtn.innerHTML = "Next";
		createQuestion();
		count++;

	} else if (questions.length === count) {
		nextBtn.innerHTML = "Generate";
		nextBtn.setAttribute("class", "btn waves-effect waves-light green");
		nextBtn.addEventListener("click", function() {
			nextBtn.setAttribute("href", "preview.html");
		});
	}
});

function createQuestion() {
	var qLabel;
	var qLabelContent;
	var p;
	var input;
	var aLabel;
	var aLabelContent;

	qLabel = document.createElement("label");
	qLabelContent = document.createTextNode(questions[count]["label"]);
	qLabel.appendChild(qLabelContent);
	caseForm.insertBefore(qLabel, btnContainer);

	for(var i = 0; i < questions[count]["answer"].length; i++) {
		p = document.createElement("p");
		input = document.createElement("input");
		input.setAttribute("type", questions[count]["type"]);
		input.setAttribute("name", questions[count]["name"]);
		input.setAttribute("id", questions[count]["aId"][i]);
		input.setAttribute("value", questions[count]["answer"][i]);
		p.appendChild(input);

		aLabel = document.createElement("label");
		aLabel.setAttribute("for", questions[count]["aId"][i]);
		aLabelContent = document.createTextNode(questions[count]["answer"][i]);
		aLabel.appendChild(aLabelContent);
		p.appendChild(aLabel);
		caseForm.insertBefore(p, btnContainer);
	}

}