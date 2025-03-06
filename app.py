import gradio as gr
from load import load_flights_dataset
from Agent import Agent

flights = load_flights_dataset()
agent = Agent(flights)
conversation = []

# Define the function that interacts with the agent
def interact_with_agent(user_input):
    response = agent.say(user_input)
    conversation.append((user_input, response.text))
    
    # Format the conversation for the Chatbot component
    formatted_conversation = [(msg[0], msg[1]) for msg in conversation]
    return formatted_conversation, ""

# Define the function to clear the conversation
def clear_conversation():
    global conversation, agent
    conversation = []
    agent = Agent(flights)
    return gr.update(value=[])

with gr.Blocks(title="Thomas the Travel Agent") as interface:
    gr.Markdown("# Thomas the Travel Agent")
    chatbot = gr.Chatbot()
    user_input = gr.Textbox()
    submit_button = gr.Button("Submit")
    clear_button = gr.Button("Clear")

    user_input.submit(interact_with_agent, inputs=user_input, outputs=[chatbot, user_input])
    submit_button.click(interact_with_agent, inputs=user_input, outputs=[chatbot, user_input])
    clear_button.click(clear_conversation, outputs=chatbot)

# Launch the Gradio app
if __name__ == "__main__":
    interface.launch()