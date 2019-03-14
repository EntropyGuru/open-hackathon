# -*- coding: utf-8 -*-
"""
This file is covered by the LICENSING file in the root of this project.
"""

import sys


from os import path
from kubernetes import client, config, utils

from hackathon import RequiredFeature, Component, Context
from hackathon.constants import HEALTH, HEALTH_STATUS, HACKATHON_CONFIG, CLOUD_PROVIDER
from hackathon.hazure import ServiceAdapter

sys.path.append("..")

__all__ = ["K8SServiceAdapter"]

class K8SServiceAdapter(ServiceAdapter):

    def __init__(self, config_file):

        self.default_config_file = "./kubeconfig.json"
        self.k8s_client = client.ApiClient()

        try:
            if config_file == None : config_file = self.default_config_file
            config.load_kube_config(config_file)
            self.k8s_api = client.AppsV1Api(client.ApiClient(config))
        except Exception as e:
            self.log.error(e)
            return False
        return True

    def create_k8s_deployment_with_yaml(self, yaml, name, namespace):
        try:
            #k8s_api is reinitialized with create_from_yaml
            self.k8s_api = utils.create_from_yaml(self.k8s_client, yaml)
            #see https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/AppsV1Api.md#read_namespaced_deployment
            resp = self.k8s_api.read_namespaced_deployment(name, namespace)
            return format(deps.metadata.name)
        except Exception as e:
            if 'Confilct' == e.reason:
                return name
            else:
                self.log.error(e)
                return None

    def deployment_exists(self, name):
        return name in list_deployments(name)

#        v1 = client.ExtensionsV1beta1Api()
#        ret = v1.list_deployment_for_all_namespaces(watch=False)
#        for i in ret.items:
#            if name == i.metadata.name:
#                return true
#        return false

    def report_health(self):
        raise NotImplementedError()



    def start_k8s_service(self, name, namespace):
        raise NotImplementedError()


    def stop_k8s_service(self):
        raise NotImplementedError()


    def ping(self, url, timeout=20):
         try:
            req = requests.get(url, timeout=timeout)
            return req.status_code == 200 and req.content == 'OK'
         except Exception as e:
            return False


#    def get_deployment_detail_by_name(self, deployment_name):
#        return

    def list_deployments(self, deployment_name, timeout=20):
        list = []
        v1 = client.ExtensionsV1beta1Api()
        #see https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/AppsV1Api.md#list_deployment_for_all_namespaces
        ret = v1.list_deployment_for_all_namespaces(watch=False)

        for i in ret.items:
            list.append(i.metadata.name)

        return list

    def get_deployment_by_name(self, deployment_name, namespace):
        #https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/AppsV1Api.md#read_namespaced_deployment
        deps = self.k8s_api.read_namespaced_deployment(deployment_name, namespace)
        return deps.metadata.available

#if __name__ == '__main__':
#    main()
