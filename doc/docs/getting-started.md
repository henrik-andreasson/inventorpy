

# Getting started

* Start as described above.
* Register first user (currently there is no admin, all users can to everything, but everything is logged through audit log)
* Optionally turn off Open registration (then an existing user must create new users)
* First create the objects used by lots of other objects
  * Services
  * Locations
  * Racks
  * Network
* Now regular object can be creates, such as:
  * servers
  * firewalls
  * switches
* Optionally create physical security objects:
  * Safe
  * Compartment (locked box dedicated to one person inside a safe)
* Hardware Security Modules (HSMs)
  * HSM Domain a virtual object but all other objects belong to one of these
  * HSM PCI Card
  * HSM Backup Unit
  * HSM PED Key
  * HSM PIN
