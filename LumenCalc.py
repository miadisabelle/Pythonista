import ui

class LumenCalcView(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'LumenCalc'
        self.background_color = '#f0f0f0' # Light grey background

        # Bill Amount Input
        self.bill_label = ui.Label(frame=(20, 20, 100, 32))
        self.bill_label.text = 'Bill Amount:'
        self.bill_label.font = ('<System>', 16)
        self.add_subview(self.bill_label)

        self.bill_tf = ui.TextField(frame=(140, 20, 200, 32))
        self.bill_tf.placeholder = 'e.g., 50.00'
        self.bill_tf.keyboard_type = 'decimal_pad'
        self.bill_tf.border_width = 1
        self.bill_tf.border_color = '#cccccc'
        self.bill_tf.corner_radius = 5
        self.add_subview(self.bill_tf)

        # Tip Percentage Input
        self.tip_label = ui.Label(frame=(20, 70, 100, 32))
        self.tip_label.text = 'Tip %:'
        self.tip_label.font = ('<System>', 16)
        self.add_subview(self.tip_label)

        self.tip_tf = ui.TextField(frame=(140, 70, 200, 32))
        self.tip_tf.placeholder = 'e.g., 15'
        self.tip_tf.keyboard_type = 'number_pad'
        self.tip_tf.text = '15' # Default tip
        self.tip_tf.border_width = 1
        self.tip_tf.border_color = '#cccccc'
        self.tip_tf.corner_radius = 5
        self.add_subview(self.tip_tf)

        # Calculate Button
        self.calc_button = ui.Button(frame=(100, 130, 150, 40))
        self.calc_button.title = 'Calculate Tip'
        self.calc_button.background_color = '#007aff' # iOS blue
        self.calc_button.tint_color = 'white'
        self.calc_button.corner_radius = 8
        self.calc_button.action = self.calculate_tip # Link action to method
        self.add_subview(self.calc_button)

        # Results Display
        self.tip_amount_label = ui.Label(frame=(20, 190, 320, 24))
        self.tip_amount_label.text = 'Tip: $0.00'
        self.tip_amount_label.font = ('<System>', 18)
        self.add_subview(self.tip_amount_label)

        self.total_amount_label = ui.Label(frame=(20, 220, 320, 24))
        self.total_amount_label.text = 'Total: $0.00'
        self.total_amount_label.font = ('<System>-Bold', 20)
        self.add_subview(self.total_amount_label)

    def calculate_tip(self, sender):
        try:
            bill_amount = float(self.bill_tf.text)
            tip_percentage = float(self.tip_tf.text) / 100

            tip_amount = bill_amount * tip_percentage
            total_amount = bill_amount + tip_amount

            self.tip_amount_label.text = f'Tip: ${tip_amount:.2f}'
            self.total_amount_label.text = f'Total: ${total_amount:.2f}'
        except ValueError:
            self.tip_amount_label.text = 'Tip: Invalid Input'
            self.total_amount_label.text = 'Total: Invalid Input'
        except Exception as e:
            self.tip_amount_label.text = 'Error'
            self.total_amount_label.text = f'Error: {e}'

def main():
    # Create an instance of our view
    v = LumenCalcView()
    # Present the view as a sheet (modal presentation)
    v.present('sheet')

if __name__ == '__main__':
    main()
