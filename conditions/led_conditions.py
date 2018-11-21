"""
led_conditions

Contains the LEDConditions class
"""

import logging
from pubsub import pub
from condition import Condition

LOGGER = logging.getLogger(__name__)

CONDITION_CLASS_NAME = 'LEDConditions'

LED_CONSTANTS = {
    'orange': '1255000050',
    'red': '1255000000',
    'blue': '1000255000',
    'purple': '1255255000',
    'on': '1200200200',
    'off': '0000000000',
    'faststrobe': '4000000000001',
    'mediumstrobe': '4000000000010',
    'slowstrobe': '4000000000020'
}

class LEDConditions(Condition):
    """
    LEDConditions

    Conditions for controlling LED light strips
    """

    def __init__(self, scheduler, schedule=None):
        """
        Constructor
        """

        super().__init__(scheduler, schedule=None)
        pub.subscribe(self.evaluate, 'messages.unix_socket_node')
        LOGGER.debug('Initialized')

    def evaluate(self, msg):
        """
        Handler for receiving messages
        """

        LOGGER.info('Evaluating')
        LOGGER.debug(msg['content'])

        if 'LED' in msg['content']:
            for key in LED_CONSTANTS:
                if key in msg['content']:
                    message = LED_CONSTANTS[key]
                    LOGGER.debug(f'Sending message {message}')
                    pub.sendMessage('arduino_node.send', msg={
                        'device_code': 'LED',
                        'device_id': '101010',
                        'data': message
                    })
                    break
