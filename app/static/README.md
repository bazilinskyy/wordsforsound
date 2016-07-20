wordsforsound
=========

This application is meant to support the process of creation/design of auditory assets. The traditional approach in making such assets is following and unstructured and undocumented process of communication between persons that need the sound to be made and persons that design/create the sound. This solution offers the iterative workflow supported by tags and tagged audible examples of auditory assets and sounds.

Installation
------------

Coming soon

Running
-------

Coming soon

Use
-------
User must register to use the application at `register`. All views in the application can be views by logged in users only.

#### Workflow
Sound creation with use of the application follows a cycle `description` -> `iteration` -> `verification`. Users participating in the creation process can be notified by email when they need to take action for a particular asset.

In order to create an asset one needs to add a project at `add_project`. After a new project has been added the user can add assets to the project at `add_asset`.

#### Homepage
After logging in the user it redirected to the home page at `index`. This page contains a list of active assets, which are in one of three stages of the workflow `description`, `iteration`, `verification`. If an asset that the user is working on is not "in hands" of the user, i.e. another user needs to send the asset further along the workflow process, the asset is shown in the list `in other hands`.

#### Projects
New projects can be added at `add_project`. Project cannot be deleted.

#### Assets
New asset can be added at `add_asset`. Assets cannot be deleted, but they can be marked as finished at the verification stage.

#### Tags
The database contains tags, which can be used for descriptions of assets and tagging sounds. A list of all tags is available at `tags`. New tag can be added at `add_tag`. Tags can be deleted at `delete_tag`.

#### Sounds
The database contains sounds, which serve as examples for description of assets. A list of all sounds is available at `sounds`. New sound can be added at `add_sound`. Sounds can be tagged with tags in the database. Each sound must be in one of sound families and it need to be of one of sound types. Sounds can be deleted at `delete_sound`.
