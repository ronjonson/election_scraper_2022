from dataclasses import dataclass, field, fields

@dataclass
class Location:
    COUNTRY: str = field(default='PHILIPPINES')
    REGION: str = field(default=None)
    province: str = field(default=None)
    city: str = field(default=None)
    barangay: str = field(default=None)
    precinct: str = field(default=None)

    def __post_init__(self):
        # Retrieve the fields in the class in their defined order
        all_fields = [f.name for f in fields(self) if f.name != "COUNTRY"]
        for i, field_name in enumerate(all_fields):
            field_value = getattr(self, field_name)
            # Ensure no lower hierarchy field is set if a higher one is None
            if field_value is None:
                for lower_field in all_fields[i+1:]:
                    if getattr(self, lower_field) is not None:
                        raise ValueError(
                            f"{field_name.capitalize()} must be specified before {lower_field.capitalize()}."
                        )

    def __setattr__(self, name, value):
        all_fields = [f.name for f in fields(self)]
        if name in all_fields:
            # Set the value for the current field
            super().__setattr__(name, value)
            # Reset lower hierarchy fields
            current_index = all_fields.index(name)
            for lower_field in all_fields[current_index + 1:]:
                super().__setattr__(lower_field, None)
        else:
            super().__setattr__(name, value)

    def get_start_location(self) -> dict:
        location = {}
        for field in fields(self):
            field_name = field.name
            field_value = getattr(self, field_name)
            if field_value is None:
                return location
            location[field_name] = field_value
        return location



    def save_current_location(self):
        pass