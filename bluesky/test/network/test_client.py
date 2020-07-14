"""
Tests for the BlueSky client base class.

Run from the command line (from the project root 'bluesky' directory):
pytest bluesky/test/network/test_client.py

Run from an IDE:
Run configuration must specify the working directory to be the project root 'bluesky' directory,
otherwise the attempt to start the BlueSky server will fail inside the addnodes() method (in server.py).

Author <thobson@turing.ac.uk> Tim Hobson
"""

import pytest
import time
import sys
import os

from bluesky.network import Client, Server

EVENT_PORT = 9000
STREAM_PORT = 9001

# Aircraft ID and altitude:
acid = '1000'
altitude = 17000



@pytest.fixture(scope="function")
def server():
    """Start the server in headless mode."""

    try:
        server = Server(True, "settings.cfg")
        server.start()
        print("Server started with host_id: {}".format(server.host_id))
    except Exception as e:
        print(e)
        sys.exit(1)
    return server


def shutdown_server(server):
    """Wait for the server thread to terminate.
    Make sure there are no spawned_processes else this will hang."""

    for n in server.spawned_processes:
        n.kill()
    server.join()


def get_client():
    """Get a Client instance, connected to the server."""

    try:
        client = Client()
        client.connect(event_port=EVENT_PORT, stream_port=STREAM_PORT)
    except Exception as e:
        print(e)
        sys.exit(1)
    return client


def test_send_event_quit(server):
    """Send the 'QUIT' event."""

    try:
        target = get_client()
        assert server.running, "Server not running, but should be"

        target.send_event(b'QUIT')

        # Wait for the QUIT event to be processed.
        time.sleep(0.1)

        assert not server.running, "Server running, but shouldn't be"

    finally:
        shutdown_server(server)


def poll_for_position(client, server, acid_, attr_name, target_string, timeout=10):
    """ Poll the server for aircraft position.

    Keyword arguments:
        client -- a Client instance
        server -- a Server instance
        acid -- an aircraft ID
        attr_name -- name of attribute to be added to client; will contain the result text returned by the POS command
        target_string -- a target string to be sought in the info returned by the POS command (default 'Info on <acid>')
        timeout -- a timeout in seconds

    This function will not return until the target_string is found in the result text returned by the POS command.
    """

    # Initialise an attribute in the client instance to hold the textual data returned by the POS command.
    setattr(client, attr_name, "")

    # Define a subscriber function to watch the client for 'ECHO' events in
    # which the payload contains a dictionary with a non-empty 'text' entry.
    def event_subscriber(name, data, sender_id):
        if name == b'ECHO':
            if isinstance(data, dict) and 'text' in data and data['text'] != '':
                setattr(client, attr_name, data['text'])

    # Add the subscriber function to the client's event_received Signal,
    # so it's triggered by the default event handler.
    # In practice, one would instead override the Client event() method.
    client.event_received.connect(event_subscriber)

    # Define the POS command to poll for aircraft location.
    pos_command_data = 'POS ' + acid_

    # Keep polling until the target string is found in the result text.
    done = False
    start_time = time.time()
    while not done and time.time() < start_time + timeout:
        try:
            # Poll for aircraft location.
            client.send_event(b'STACKCMD', pos_command_data, target=b'*')
            client.receive()

            # This pause is not strictly necessary but avoids excessive polling before the server is ready.
            time.sleep(0.1)

            # Check that the client's servers dictionary is no longer empty.
            assert len(client.servers) == 1, "Client's servers dictionary should have one element"
            assert server.host_id in client.servers

            # Seek the target string in the textual data returned by the POS command.
            if getattr(client, attr_name).find(target_string) != -1:
                # Print the full text to the console.
                print("Target string found in POS response text:\n" + str(getattr(client, attr_name)))
                done = True

        except KeyboardInterrupt:
            sys.exit(0)
    return

def reset_sleep():
    """Get the sleep duration after RESET."""

    if 'RESET_SLEEP' in os.environ:
        return int(os.getenv('RESET_SLEEP'))
    return 2


def test_send_event_stackcmd_cre_pos(server):
    """ Send the 'STACKCMD' event to create an aircraft & poll for its position. """

    try:
        target = get_client()

        # Reset the simulation
        target.send_event(b'STACKCMD', 'RESET', target=b'*')

        # Wait for the RESET event to be processed.
        # Omitting this line breaks the test; in that case the text response to the POS
        # command is constantly: "BlueSky Console Window: Enter HELP or ? for info."
        time.sleep(reset_sleep())

        # Create an aircraft with a particular ID and altitude.
        cre_command_data = 'CRE {} 0 0 0 0 {} 500'.format(acid, str(altitude))
        target.send_event(b'STACKCMD', cre_command_data, target=b'*')

        assert target.sender_id == b'', "Client's sender_id differs from default (empty) value"
        assert not target.servers, "Client's servers dictionary should be empty, but isn't"

        # Define an attribute name to hold the result (i.e. the text returned by the POS command).
        attr_name = "result"

        # Poll for aircraft position information.
        poll_for_position(target, server, acid, attr_name, 'Info on {}'.format(acid))

        # Check the result, i.e. the text returned by the POS command.
        result = getattr(target, attr_name)
        assert result.find('Info on {}'.format(acid)) != -1, "Failed to find aircraft ID information"
        assert result.find('Alt: {} ft'.format(str(altitude))) != -1, "Failed to find aircraft altitude information"

    finally:
        target.send_event(b'QUIT')
        shutdown_server(server)


@pytest.fixture(scope="function")
def scenario_filename(tmpdir):
    """Write a temporary file containing scenario content and return the filename."""

    scenario_content = \
        ("00:00:00.00>OP\n"
         "00:00:00.00>HOLD\n"
         "00:00:00.00>SSD ALL\n"
         "00:00:00.00>ZOOM OUT 100\n"
         "00:00:00.00>PAN 0 0\n\n"
         "00:00:00.00>CRE {} B744 0 0 0 {} 250\n\n"
         "00:00:00.00>OP").format(acid, str(altitude))

    p = tmpdir.mkdir("scenario").join("scenario.scn")
    p.write(scenario_content)
    return p


def test_send_event_stackcmd_ic_alt(server, scenario_filename):
    """ Send the 'STACKCMD' event to initialise a scenario & order a change of altitude. """

    # Check the (temporary) scenario file exists.
    # Note that the IC command only accepts a filename argument.
    assert os.path.isfile(scenario_filename)

    try:
        target = get_client()

        # Reset the simulation
        target.send_event(b'STACKCMD', 'RESET', target=b'*')

        # Wait for the RESET event to be processed.
        # Omitting this line breaks the test; in that case the text response to the POS
        # command is constantly: "BlueSky Console Window: Enter HELP or ? for info."
        time.sleep(reset_sleep())

        # Initialise the scenario.
        target.send_event(b'STACKCMD', 'IC {}'.format(scenario_filename), target=b'*')

        # Define an attribute name to hold the result (i.e. the text returned by the POS command).
        attr_name = "result"

        # Poll for aircraft position information.
        poll_for_position(target, server, acid, attr_name, 'Info on {}'.format(acid))

        # Check the aircraft is at the expected altitude
        result = getattr(target, attr_name)
        assert result.find('Info on {}'.format(acid)) != -1, "Failed to find aircraft ID information"
        assert result.find('Alt: {} ft'.format(str(altitude))) != -1, "Failed to find aircraft altitude information"

        # Send an ALT command to instruct the aircraft to ascend.
        new_altitude = altitude + 10
        alt_command = 'ALT {} {}'.format(acid, new_altitude)
        target.send_event(b'STACKCMD', alt_command, target=b'*')

        # Poll for aircraft position information, terminating only when the new altitude is reported.
        target_string = 'Alt: {} ft'.format(str(new_altitude))
        poll_for_position(target, server, acid, attr_name, target_string)

        # Check the aircraft is at the new altitude.
        result = getattr(target, attr_name)
        assert result.find('Info on {}'.format(acid)) != -1, "Failed to find aircraft ID information"
        assert result.find('Alt: {} ft'.format(str(new_altitude))) != -1, "Failed to verify new aircraft altitude"

        assert new_altitude != altitude, "Original and new altitudes must not be equal"

    finally:
        target.send_event(b'QUIT')
        shutdown_server(server)
