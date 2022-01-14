zpa\_segment\_group module
==========================

zpa_segment_group-- Create/Update/Delete an Segment Group.
========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create/Update/Delete an Segment Group.

.. automodule:: zpa_segment_group
   :members:



Parameters
----------

  name: (required: type: str)
   Name of the application.


Notes
-----




.. code-block:: yaml

    - name: Create/Update/Delete a Server Group
      willguibr.zpacloud.zpa_segment_group:
        config_space: "DEFAULT"
        name: Example Segment Group
        description: Example Segment Group
        enabled: true
        policy_migrated: true
        tcp_keep_alive_enabled: "1"

Status
------





Authors
~~~~~~~

- William Guilherme (@willguibr)
