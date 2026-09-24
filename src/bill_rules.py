# AWS prices - eu-west-2 (London), On-Demand
# Checked 15 September 2026

T3_MICRO_PER_HOUR = 0.0118
T3_SMALL_PER_HOUR = 0.0236
T3_MEDIUM_PER_HOUR = 0.0472

NAT_PER_HOUR = 0.05
NAT_PER_GB = 0.05

DB_T3_MICRO_PER_HOUR = 0.019
DB_T3_SMALL_PER_HOUR = 0.038
DB_STORAGE_PER_GB_MONTH = 0.133
TRANSFER_PER_GB = 0.09
FREE_TRANSFER_GB = 100

S3_PER_GB_MONTH = 0.024



def ec2_cost(price_per_hour,hours):
    return price_per_hour*hours




def nat_gateway_cost(nat_per_hour,hours,nat_per_gb,gb_transferred):
    return (nat_per_hour*hours)+(nat_per_gb*gb_transferred)




def s3_cost (price_per_gb_month,gb_store):
    return(price_per_gb_month*gb_store)



def rds_cost(db_price_per_hour,hours,storage_price_per_gb_month,gb_stored):
    return(db_price_per_hour*hours)+(storage_price_per_gb_month*gb_stored)


def data_transfer_cost(price_per_gb, gb_out, free_gb):
    if gb_out <= free_gb:
        return 0
    else:
        return (price_per_gb *(gb_out-free_gb))   


def assess(server_type, hours, db_type, db_hours, nat, gb_stored, gb_out):
    try:
        hours = float(hours)
        gb_stored = float(gb_stored)
        gb_out = float(gb_out)
        db_hours = float(db_hours)
    except ValueError:
        return {"error": "Please enter numbers only for hours and gigabytes."}

    if hours < 0 or db_hours < 0 or gb_stored < 0 or gb_out < 0:
         return {"error": "Please enter zero or more. Negative numbers don't make sense here."}
    
    if server_type == "t3.micro":
        server_price = T3_MICRO_PER_HOUR
    elif server_type == "t3.small":
        server_price = T3_SMALL_PER_HOUR
    elif server_type == "t3.medium":
        server_price = T3_MEDIUM_PER_HOUR
    else:
        server_price = 0


    if db_type == "db.t3.micro":
        db_price =DB_T3_MICRO_PER_HOUR
    elif db_type == "db.t3.small":
        db_price = DB_T3_SMALL_PER_HOUR
    else:
        db_price = 0    

    if db_type == "none":
        db_total = 0
    else:
        db_total = rds_cost(db_price, db_hours, DB_STORAGE_PER_GB_MONTH, 20)

    server_total = ec2_cost(server_price, hours)
    s3_total = s3_cost(S3_PER_GB_MONTH, gb_stored)
    transfer_total = data_transfer_cost(TRANSFER_PER_GB, gb_out, FREE_TRANSFER_GB)

    if nat == "yes":
        nat_total = nat_gateway_cost(NAT_PER_HOUR, 730 , NAT_PER_GB, gb_out)
    else:
        nat_total = 0

    total = server_total + db_total + nat_total + s3_total + transfer_total

    breakdown = [
        ("Server", server_total),
        ("Database", db_total),
        ("NAT gateway", nat_total),
        ("Storage", s3_total),
        ("Data transfer", transfer_total),
    ]

    breakdown.sort(key=lambda item: item[1], reverse=True)

    warnings = []

    if nat == "yes":
        warnings.append("A NAT gateway charges by the hour just for existing. There is no stop button the only way to stop paying is to delete it")

    if gb_out > FREE_TRANSFER_GB:
        warnings.append(f"You have exceeded the free data transfer allowance of {FREE_TRANSFER_GB}GB. You will be charged for {gb_out - FREE_TRANSFER_GB}GB of data transfer.")


    return {
        "total": total,
        "breakdown": breakdown,
        "warnings": warnings,
    }


    