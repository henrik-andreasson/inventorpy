

# Getting started

1. Start as described above.
2. Register first user (currently there is no admin, all users can to everything, but everything is logged through audit log)
3. Optionally turn off Open registration (then an existing user must create new users)
4. First create the objects used by lots of other objects
  * Services
  * Locations
  * Racks
  * Network
5. Now regular object can be creates, such as:
  * servers
  * firewalls
  * switches
6. Optionally create physical security objects:
  * Safe
  * Compartment (locked box dedicated to one person inside a safe)
7. Hardware Security Modules (HSMs)
  * HSM Domain a virtual object but all other objects belong to one of these
  * HSM PCI Card
  * HSM Backup Unit
  * HSM PED Key
  * HSM PIN
