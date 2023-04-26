import numpy as np
import torch
import gradio as gr

from lenia.discrete_lenia import DiscreteLenia


# def flip_text(x):
#     return x[::-1]


# def flip_image(x):
#     return np.fliplr(x)


# with gr.Blocks() as lenia_demo:
#     gr.Markdown("Lenia Implementation")
#     with gr.Tab("Flip Text"):
#         text_input = gr.Textbox()
#         text_output = gr.Textbox()
#         text_button = gr.Button("Flip")
#     with gr.Tab("Flip Image"):
#         with gr.Row():
#             image_input = gr.Image()
#             image_output = gr.Image()
#         image_button = gr.Button("Flip")

#     with gr.Accordion("Open for More!"):
#         gr.Markdown("Look at me...")

#     text_button.click(flip_text, inputs=text_input, outputs=text_output)
#     image_button.click(flip_image, inputs=image_input, outputs=image_output)

LENIA_GRID = None

def get_lenia(grid_x, grid_y, space_res, time_res, state_res, kernel_core_name, kernel_peaks_text,
              growth_mapping_name, growth_center, growth_width):
    kernel_peaks = [float(num.strip()) for num in kernel_peaks_text.split(',')]
    kernel_peaks = torch.Tensor(kernel_peaks)
    global LENIA_GRID
    if LENIA_GRID is None:
        LENIA_GRID = DiscreteLenia(grid_x, grid_y, space_res, time_res, state_res,
                                kernel_core_name.lower(), kernel_peaks, growth_mapping_name.lower(),
                                growth_center, growth_width)
        kernel = LENIA_GRID.kernel.numpy()
        grid = LENIA_GRID.config.numpy()
        return grid
    else:
        LENIA_GRID.update()
        kernel = LENIA_GRID.kernel.numpy()
        grid = LENIA_GRID.config.numpy()
        return grid




with gr.Blocks() as lenia_demo:
    gr.Markdown("# Lenia Implementation")
    with gr.Row():
        with gr.Column():
            with gr.Row():
                conway_button = gr.Button(value="Conway's Game of Life", onclick=lambda: 0)
                # conway_button.style(size='sm', full_width=False)
                restart_button = gr.Button(value="Reset Values", onclick=lambda: 0)
                # restart_button.style(size='sm', full_width=False)
            with gr.Row():
                grid_x = gr.inputs.Number(default=32, label='Grid Width')
                grid_y = gr.inputs.Number(default=32, label='Grid Height')
            space_res = gr.inputs.Slider(minimum=0, maximum=100, step=1, default=1, label='Space Resolution')
            time_res = gr.inputs.Slider(minimum=0, maximum=100, step=1, default=1, label='Time Resolution')
            state_res = gr.inputs.Slider(minimum=0, maximum=100, step=1, default=1, label='State Resolution')
            growth_mapping_name = gr.inputs.Radio(default='Exponential', choices=['Exponential', 'Polynomial', 'Rectangular'], label='Growth Mapping')
            with gr.Row():
                growth_center = gr.inputs.Number(default=0, label='Growth Center')
                growth_width = gr.inputs.Number(default=1, label='Growth Width')
            kernel_core_name = gr.inputs.Radio(default='Exponential', choices=['Exponential', 'Polynomial', 'Rectangular'], label='Kernel Core')
            kernel_peaks_text = gr.inputs.Textbox(default="1,1,1,1,1,1,1,1", label='Kernel Peaks (Enter a list of numbers (0 or 1) separated by commas)')
        with gr.Column():
            output_image = gr.outputs.Image(type='numpy', label="Lenia")
            output_kernel = gr.outputs.Image(type='numpy', label="Kernel")
    inputs = [grid_x,
              grid_y,
              space_res,
              time_res,
              state_res,
              kernel_core_name,
              kernel_peaks_text,
              growth_mapping_name,
              growth_center,
              growth_width]
    print(inputs)
    outputs = [output_image, output_kernel]
    init = lenia_demo.load(get_lenia, inputs, output_image, every=1)



# inputs = [
#     gr.inputs.Number(default=0, label='Growth Center'),
#     gr.inputs.Number(default=0, label='Growth Width'),
#     gr.inputs.Slider(minimum=0, maximum=100, step=1, default=50, label='Space Resolution'),
#     gr.inputs.Slider(minimum=0, maximum=100, step=1, default=50, label='Time Resolution'),
#     gr.inputs.Slider(minimum=0, maximum=100, step=1, default=50, label='State Resolution'),
#     gr.inputs.Radio(choices=['Exponential', 'Polynomial', 'Rectangular'], label='Growth Mapping'),
#     gr.inputs.Radio(choices=['Exponential', 'Polynomial', 'Rectangular'], label='Kernel Core'),
#     gr.inputs.Textbox(label='Kernel Peaks (Enter a list of numbers (0 or 1) separated by commas)')
# ]
# # conway_button = gr.Button(label="Conway's Game of Life", onclick=lambda: 0)
# # restart_button = gr.Button(label="Reset Values", onclick=lambda: 0)
# # output = gr.outputs.Image(label='Inverted image')

# def calculate_sum(*args, **kwargs):
#     # Split the input string into a list of numbers
#     return np.array([[0,1], [1,0]])
#     # numbers_list = [float(num.strip()) for num in numbers.split(',')]

#     # # Calculate the sum of the numbers
#     # total = sum(numbers_list)

#     return total
# lenia_interface = gr.Interface(fn=calculate_sum, inputs=inputs, outputs=None, title='Lenia', live=True,)


if __name__ == '__main__':
    lenia_demo.queue().launch()
