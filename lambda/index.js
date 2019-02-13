const Alexa = require('ask-sdk-core');
const AWS = require('aws-sdk');
const util = require("util");

var commandQueueUrl;

const PushToCommandQueue = function (message) {
		let deduplicationId = Date.now().toString() + message;
		
		sqs.sendMessage({
			MessageBody: message,
			QueueUrl: commandQueueUrl,
			MessageGroupId: "SerialCommands",
			MessageDeduplicationId: deduplicationId
		}, (err, data) => {
				console.log(err);
		});
}

const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
    },
    handle(handlerInput) {
        const speechText = 'Media Control open - what would you like to do?';
        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .getResponse();
    }
};
const TestIntentRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'TestIntent';
    },
    handle(handlerInput) {
        let body = "Testing4";

				PushToCommandQueue(body);

        const speechText = 'Sending command';
        return handlerInput.responseBuilder
            .speak(speechText)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};

const SetInputRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'SetInput';
    },
    handle(handlerInput) {
        let device_name = handlerInput.requestEnvelope.request.intent.slots.device.value;
        let input_type = handlerInput.requestEnvelope.request.intent.slots.input_type.value;
        let input_number = handlerInput.requestEnvelope.request.intent.slots.input_number.value;

        let body = "SetInput:"+device_name+":"+input_type+":"+input_number;

				PushToCommandQueue(body);
       
        const speechText = 'Setting input on ' + device_name + " to " + input_type + " " + input_number;
        return handlerInput.responseBuilder
            .speak(speechText)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};

const DemonstrateRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'Demonstrate';
    },
    handle(handlerInput) {
        let body = "Demonstrate:";
        
				PushToCommandQueue(body);

        const speechText = 'Beginning demonstration';
        return handlerInput.responseBuilder
            .speak(speechText)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};

const SetPowerRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'SetPower';
    },
    handle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots
        let state = slots.state.value;
        let device = slots.device.value;
        let body = "SetPower:"+device+":"+state;
        
				PushToCommandQueue(body)

        const speechText = 'Turning the ' + device + " " + state ;
        return handlerInput.responseBuilder
            .speak(speechText)
            .withShouldEndSession(true)
            .getResponse();
    }
};


const HelpIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        const speechText = 'You can say hello to me! How can I help?';

        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .getResponse();
    }
};
const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
                || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
    },
    handle(handlerInput) {
        const speechText = 'Goodbye!';
        return handlerInput.responseBuilder
            .speak(speechText)
            .getResponse();
    }
};
const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        // Any cleanup logic goes here.
        return handlerInput.responseBuilder.getResponse();
    }
};

// The intent reflector is used for interaction model testing and debugging.
// It will simply repeat the intent the user said. You can create custom handlers
// for your intents by defining them above, then also adding them to the request
// handler chain below.
const IntentReflectorHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest';
    },
    handle(handlerInput) {
        const intentName = handlerInput.requestEnvelope.request.intent.name;
        const speechText = `You just triggered ${intentName}`;

        return handlerInput.responseBuilder
            .speak(speechText)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};

const FallbackHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        console.log(`~~~~ Error handled: ${error.message}`);
        const speechText = `Sorry, I didn't recognise that command. Please try again.`;

        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .getResponse();
    }
};

// Generic error handling to capture any syntax or routing errors. If you receive an error
// stating the request handler chain is not found, you have not implemented a handler for
// the intent being invoked or included it in the skill builder below.
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        console.log(`~~~~ Error handled: ${error.message}`);
        const speechText = `Sorry, an error has occurred. Please try again.`;

        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .getResponse();
    }
};

//============================================================================
//END HANDLERS
//============================================================================

AWS.config.update({region: "eu-west-1"});

var sqs = new AWS.SQS();
var commandQueueUrl;

const getQueueUrlPromised = util.promisify(sqs.getQueueUrl);

var commandQueueUrlPromise = new Promise(function(resolve, reject) {
    sqs.getQueueUrl({QueueName: "SerialEntertainment.fifo"}, function(error, result) {
        if(error) {
            reject(error);
        } else {
            resolve(result);
        }
    });
});

// This handler acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
let skillHandler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        TestIntentRequestHandler,
        SetPowerRequestHandler,
        SetInputRequestHandler,
        DemonstrateRequestHandler,
        HelpIntentHandler,
        CancelAndStopIntentHandler,
        SessionEndedRequestHandler,
				FallbackHandler
        //IntentReflectorHandler) // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
        )
    .addErrorHandlers(
        ErrorHandler)
    .lambda();

exports.handler = function(...theargs) {
    Promise.all([commandQueueUrlPromise]).then(
    (result) => {
        commandQueueUrl = result[0].QueueUrl;
        skillHandler(...theargs);
    },
    (error) => {
        console.error("Failed to get URL with error:", error);
    });
}

