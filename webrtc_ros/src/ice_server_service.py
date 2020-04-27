#!/usr/bin/env python

import json
import rospy
import requests
from webrtc_ros.msg import IceServer
from webrtc_ros.srv import GetIceServers, GetIceServersResponse


class IceServerManager(object):
    """ Manages providing ice server information to the webrtc system """

    def __init__(self):
        rospy.init_node('ice_server_provider')

        self.stun_servers = rospy.get_param('stun_servers', [
            'stun:stun1.l.google.com:19302', 'stun:stun2.l.google.com:19302'])
        self.turn_server_uris = rospy.get_param('turn_server_uris', '')
        self.turn_creds_uri = rospy.get_param('turn_server_creds_uri', '')
        self.turn_creds_username = rospy.get_param(
            'turn_server_creds_username', '')
        self.turn_creds_password = rospy.get_param(
            'turn_server_creds_password', '')

        self.get_ice_servers_service = rospy.Service(
            'get_ice_servers', GetIceServer, self.get_ice_servers)

        rospy.loginfo('Ice Server Provider Up')
        rospy.spin()

    def get_turn_creds(self):
        """Get the credentials from the turn server."""
        if self.turn_creds_uri:
            resp = requests.post(self.turn_creds_uri,
                                 {'username': self.turn_creds_username,
                                  'password':  self.turn_creds_password})
            if(('username' in resp.data) and ('password' in resp.data)):
                return resp.data
        return False

    def get_ice_servers(self, _):
        """Callback for service. Returns the ice servers"""
        resp = GetIceServerResponse()
        turn_creds = self.get_turn_creds()
        if turn_creds:
            for uri in self.turn_server_uris:
                serv = IceServer()
                serv.username = turn_creds['username']
                serv.password = turn_creds['password']
                resp.survers.append(serv)
        for suri in self.stun_servers:
            serv = IceServer()
            serv.uri = suri
            resp.survers.append(serv)
        return resp


if __name__ == '__main__':
    IceServerManager()