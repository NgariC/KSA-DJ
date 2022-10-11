class PaidForList:
    def units_list(self, obj):
        return "\n".join(['%d %s - %s' % (i, a.name, a.sub_county.name)
                          for i, a in enumerate(obj.units_paid_for.all(), start=1)])

    def scouts_list(self, obj):
        return "\n".join(['%d %s (%s,   %s)' % (i, a.name, a.section, a.unit.sub_county.name)
                          for i, a in enumerate(obj.scouts_paid_for.all(), start=1)])

    def scout_leaders_list(self, obj):
        return "\n".join(['%d %s (%s,   %s)' % (i, a.name, a.phone_number, a.sub_county.name)
                          for i, a in enumerate(obj.scout_leaders_paid_for.all(), start=1)])

    def itcs_list(self, obj):
        return "\n".join(['%d %s (%s - %s)' % (i, a.venue_name, a.start_date, a.sub_county.name)
                          for i, a in enumerate(obj.itcs_paid_for.all(), start=1)])

    def ptcs_list(self, obj):
        return "\n".join(['%d %s (%s - %s)' % (i, a.venue_name, a.start_date, a.sub_county.name)
                          for i, a in enumerate(obj.ptcs_paid_for.all(), start=1)])

    def investitures_list(self, obj):
        return "\n".join(['%d %s (%s - %s)' % (i, a.venue_name, a.start_date, a.sub_county.name)
                          for i, a in enumerate(obj.investitures_paid_for.all(), start=1)])

    def badge_camps_list(self, obj):
        return "\n".join(['%d %s (%s - %s)' % (i, a.venue_name, a.start_date, a.sub_county.name)
                          for i, a in enumerate(obj.badge_camps_paid_for.all(), start=1)])

    def park_holidays_list(self, obj):
        return "\n".join(['%d %s (%s - %s)' % (i, a.venue_name, a.start_date, a.sub_county.name)
                          for i, a in enumerate(obj.park_holidays_paid_for.all(), start=1)])

    def plcs_list(self, obj):
        return "\n".join(['%d %s (%s - %s)' % (i, a.venue_name, a.start_date, a.sub_county.name)
                          for i, a in enumerate(obj.plcs_paid_for.all(), start=1)])

    def rover_mates_list(self, obj):
        return "\n".join(['%d %s (%s - %s)' % (i, a.venue_name, a.start_date, a.sub_county.name)
                          for i, a in enumerate(obj.rover_mates_paid_for.all(), start=1)])
